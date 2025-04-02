import multiprocessing.pool
import os
import re
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import TextIO

import PIL.Image

from src.account_process_main import process_main
from src.logging_thread import logging
from src.structures.question_typology_class import QuestionTypology


#Legenda
# %% -> la domanda continua con un altra parte
# %%% -> la domanda termina ma la prossima sarà uguale con metodologia diversa: one-shot, CoT, PoT
# %%%% -> fine file
# %OS, %COT, %POT servono a indicare la tipologia della domanda
def get_type(file_f: TextIO) -> QuestionTypology:
    q_type: QuestionTypology
    first_line = re.sub("[\n\r\t\s]", "", file_f.readline())
    if first_line == "%OS":
        q_type = QuestionTypology.OS
    elif first_line == "%COT":
        q_type = QuestionTypology.COT
    elif first_line == "%POT":
        q_type = QuestionTypology.POT
    else:
        raise ValueError("Error: can't find the question type")
    return q_type

#TODO: gestire gli LLMs che non supportano le immagini!! potresti descrivere l'immagine.
def message_create(txt, opt_img_path):
    if opt_img_path is None:
        return [txt]
    else:
        image = PIL.Image.open(opt_img_path)
        return [image, txt]


def get_questions(file_f: TextIO, messages, opt_image_path: str | None) -> bool:
    question = ""
    for line in file_f:
        if line.replace("\n", "") == "%%":
            messages.append(message_create(question, opt_image_path))
            return get_questions(file_f, messages, None)
        elif line.replace("\n", "") == "%%%":
            messages.append(message_create(question, opt_image_path))
            return False
        elif line.replace("\n", "") == "%%%%":
            messages.append(message_create(question, opt_image_path))
            return True
        else:
            question += line
    return False


def main(file_name, file, opt_image_path, account_api_key, repetitions, model):
    # Creating the messages for Gemini from the file
    messages_list = list()
    finished = False
    while not finished:
        msg = []
        question_type = get_type(file)
        finished = get_questions(file, msg, opt_image_path)
        messages_list.append((msg, question_type))
    file.close()
    # Starting the processes
    question_name = re.sub(r"src\\..\\..\\questions\\typology" + "[0-9]" + r"\\", "", file_name).replace(".txt", "")
    processes = list()
    processes_pool = multiprocessing.pool.Pool()
    logging_threads = list()
    logging_threads_pool = ThreadPool()
    manager = Manager()
    for i, ak in enumerate(account_api_key):
        log_msg_qq = manager.Queue()
        Path("src\\..\\..\\response\\" + model + "\\" + "account" + str(i) + "\\" + question_name).mkdir(parents=True, exist_ok=True)
        log_file_name = "src\\..\\..\\response\\"+model+"\\" + "account" + str(i) + "\\response_log.txt"
        if not os.path.isfile(log_file_name):
            log_file = open(log_file_name, "x")
            log_file.write(
                "This file explains when the tests were carried out, the dates are expressed: [year-month-day].\n\n")
            log_file.flush()
            log_file.close()
        logging_threads.append(logging_threads_pool.apply_async(logging, args=[question_name.replace(".txt", ""), log_file_name, log_msg_qq]))

        processes.append(processes_pool.apply_async(process_main, args=(
            ak, question_name, "account" + str(i), messages_list, repetitions, model, log_msg_qq
                                                                    )))


    for p in processes:
        p.get()
        p.wait()

    processes_pool.join()

    for t in logging_threads:
        t.wait()

    logging_threads_pool.join()