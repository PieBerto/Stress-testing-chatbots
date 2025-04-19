import re
from multiprocessing import Process
from typing import TextIO

import PIL.Image
from PIL.ImageFile import ImageFile

from src.account_process_main import process_main
from src.logging_thread import LoggingThread
from src.structures import tools
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
#TODO: racchiudere counter e logging in una classe contenente le due code e le funzioni da invocare
def message_create(txt: str, opt_img_path) -> str | list[ImageFile | str]:
    if opt_img_path is None:
        return txt
    else:
        image = PIL.Image.open(opt_img_path)
        return [image, txt]


def get_questions(file_f: TextIO, messages: list[str | list[ImageFile, str]], opt_image_path: str | None) -> bool:
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
    messages_list: list[tuple[list[str | list[ImageFile, str]], QuestionTypology]] = list()
    finished = False
    while not finished:
        msg: list[str | list[ImageFile, str]] = []
        question_type = get_type(file)
        finished = get_questions(file, msg, opt_image_path)
        messages_list.append((msg, question_type))
    file.close()
    # Starting the processes
    base_path = "src\\..\\..\\response\\" + model + "\\" + "account "
    question_name = re.sub(r"src\\..\\..\\questions\\typology" + "[0-9]" + r"\\", "", file_name).replace(".txt", "")
    processes = list()
    logging_threads = LoggingThread(question_name.replace(".txt", ""),list(map(tools.digest,account_api_key)), base_path)

    for ak in account_api_key:
        hash_ak = str(tools.digest(ak))

        processes.append(Process(target=process_main, args=(
            ak, question_name, "account " + hash_ak, messages_list, repetitions, model, logging_threads.get(hash_ak)
        ), name="account " + hash_ak))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    logging_threads.join_all()