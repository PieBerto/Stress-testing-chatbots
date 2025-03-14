import re
from datetime import datetime
from multiprocessing import Queue

from sample.structures.question_typology_class import QuestionTypology


def logging_modify_line(lines, index, type_str, file):
    found = False
    inner_index = index
    while inner_index<len(lines) and lines[inner_index].startswith("\t\t"):
        match = re.search(str(type_str) + r"\s(\d+)", lines[inner_index])
        if match is not None:
            found = True
            num = int(match.group(1))
            lines[inner_index] = re.sub("[1-9][0-9]*", str(num + 1), lines[inner_index])
        inner_index += 1
    if not found:
        lines.insert(index, "\t\t" + type_str + " 1" + "\n")
    #DEBUG purpose
    #print(lines)
    file.writelines(lines)
    file.flush()


def logging(question_name: str, log_file_name: str, log_msg_qq: Queue):
    msg = "start"
    while msg != "TERMINATE":
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
        msg = log_msg_qq.get()
        backup = lines
        try:
            log_file = open(log_file_name, "w")
            match msg:
                case QuestionTypology.OS:
                    logging_modify_line(lines, found, "OS", log_file)
                case QuestionTypology.COT:
                    logging_modify_line(lines, found, "COT", log_file)
                case QuestionTypology.POT:
                    logging_modify_line(lines, found, "POT", log_file)
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