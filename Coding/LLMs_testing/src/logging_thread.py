import os
import re
from datetime import datetime
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from pathlib import Path

from filelock import FileLock

from src.structures.question_typology_class import QuestionTypology

class LoggingThread:
    def __init__(self, question_name:str, hash_keys: list[str], base_path:str):
        self.manager = Manager()
        self.question_name = question_name
        self.loggers_future = list()
        self.interacters = list()
        self.thread_pool = ThreadPool(processes=len(hash_keys))
        for hash_key in hash_keys:
            Path(base_path + hash_key + "\\" + question_name).mkdir(parents=True, exist_ok=True)
            log_file_name = base_path + hash_key + "\\response_log.txt"
            self.__start_logger(log_file_name, hash_key)
        self.thread_pool.close()

    def __start_logger(self, log_file_name:str, hash_key:str):
        if not os.path.isfile(log_file_name):
            lock = FileLock(log_file_name+".lock")
            with lock:
                log_file = open(log_file_name, "x")
                log_file.write(
                    "This file explains when the tests were carried out, the dates are expressed: [year-month-day].\n\n")
                log_file.flush()
                log_file.close()
        queue = self.manager.Queue()
        self.interacters.append(LoggerInteracter(hash_key,queue))
        logger = _Logger(log_file_name, hash_key, self.question_name ,queue)
        self.loggers_future.append(self.thread_pool.apply_async(logger.logging))

    def join_all(self):
        for l in self.loggers_future:
            l.wait()
        self.thread_pool.join()

    def get(self, hash_key:str):
        for i in self.interacters:
            if i.hash_key == hash_key:
                return i


class _Logger:
    def __init__(self, log_file_name:str, hash_key: str, question_name: str, queue):
        self.log_file_name = log_file_name
        self.hash_key = hash_key
        self.question_name = question_name
        self.queue = queue


    def logging(self):
        (question_name, log_msg_qq, log_file_name) = (self.question_name, self.queue, self.log_file_name)
        msg = "start"
        while msg != "TERMINATE":
            msg = log_msg_qq.get()
            lock = FileLock(log_file_name+".lock")
            with lock:
                log_file = open(log_file_name,"r")
                lines = log_file.readlines()
                log_file.close()
                found: int = -1
                try:
                    start = index = lines.index(question_name+"\n") + 1
                    while index < len(lines) and lines[index].startswith("\t"):
                        if lines[index].startswith("\t" + datetime.today().strftime('%Y-%m-%d')):
                            found = index + 1
                            break
                        index += 1
                    if found == -1:
                        lines.insert(start, "\t" + datetime.today().strftime('%Y-%m-%d') + "\n")
                        found = start +1
                except ValueError:
                    lines.append(question_name + "\n")
                    lines.append("\t" + datetime.today().strftime('%Y-%m-%d') + "\n")
                    lines.append("\n")
                    found = len(lines) - 1
                backup = lines
                try:
                    log_file = open(log_file_name, "w")
                    match msg:
                        case QuestionTypology.OS:
                            self.__logging_modify_line(lines, found, "OS", log_file)
                        case QuestionTypology.COT:
                            self.__logging_modify_line(lines, found, "COT", log_file)
                        case QuestionTypology.POT:
                            self.__logging_modify_line(lines, found, "POT", log_file)
                        case "TERMINATE":
                            log_file.writelines(lines)
                            log_file.close()
                        case _:
                            raise ValueError("Wrong message in logging thread, msg: " + msg)
                except Exception as e:
                    print("Exception occurred while writing the log file:\n", str(e))
                    log_file.truncate(0)
                    log_file.writelines(backup)
                    log_file.flush()
                log_file.close()

    @staticmethod
    def __logging_modify_line(lines, index, type_str, file):
        found = False
        inner_index = index
        while inner_index < len(lines) and lines[inner_index].startswith("\t\t"):
            match = re.search(str(type_str) + r"\s(\d+)", lines[inner_index])
            if match is not None:
                found = True
                num = int(match.group(1))
                lines[inner_index] = re.sub("[1-9][0-9]*", str(num + 1), lines[inner_index])
            inner_index += 1
        if not found:
            lines.insert(index, "\t\t" + type_str + " 1" + "\n")
        # DEBUG purpose
        # print(lines)
        file.writelines(lines)
        file.flush()

class LoggerInteracter:
    def __init__(self, hash_key:str, queue):
        self.hash_key = hash_key
        self.queue = queue

    def send_msg(self, msg: str | QuestionTypology):
        self.queue.put(msg)

    def terminate(self):
        self.send_msg("TERMINATE")