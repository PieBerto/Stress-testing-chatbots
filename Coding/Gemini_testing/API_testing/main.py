import os
import re
import threading
from multiprocessing import Process
from multiprocessing import Queue
from pathlib import Path
from typing import TextIO

import PIL.Image

from API_testing.logging_main_thread import logging
from API_testing.processes_main import process_main
from API_testing.structures.question_typology_class import QuestionTypology

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
    question_name = re.sub(r"..\\questions\\typology" + "[0-9]" + r"\\", "", file_name).replace(".txt", "")
    processes = list()
    logging_threads = list()
    for i, ak in enumerate(account_api_key):
        log_msg_qq = Queue()
        processes.append(Process(target=process_main, args=(
            ak, question_name, "account" + str(i), messages_list, repetitions, model, log_msg_qq
        ), name="account" + str(i)))
        Path("..\\response\\" + model + "\\" + "account" + str(i) + "\\" + question_name).mkdir(parents=True, exist_ok=True)
        log_file_name = "C:\\GitHub\\Stress-testing-chatbots\\Coding\\response\\"+model+"\\" + "account" + str(i) + "\\response_log.txt"
        if not os.path.isfile(log_file_name):
            log_file = open(log_file_name, "x")
            log_file.write(
                "This file explains when the tests were carried out, the dates are expressed: [year-month-day].\n\n")
            log_file.flush()
            log_file.close()
        logging_threads.append(threading.Thread(target=logging, args=[question_name.replace(".txt", ""), log_file_name, log_msg_qq],
                                          name="account" + str(i) + "_logging"))
    for t in logging_threads:
        t.start()

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("Processes joined")

    for t in logging_threads:
        t.join()

    print("Logging threads joined")