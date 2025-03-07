import os
import random
import argparse
import re
import sys
import time
from google.genai import Client
from multiprocessing import Process
from typing import TextIO
from io import StringIO
from google import genai
from google.ai.generativelanguage_v1 import GenerateContentResponse
from google.api_core.exceptions import ResourceExhausted, InternalServerError, DeadlineExceeded
from pathlib import Path
from enum import Enum
import PIL.Image

#TODO: mancano le apikey non hardcoded ma da leggere in un file esterno al progetto e la scrittura di un file di log

class QuestionTypology(Enum):
    OS = "one-shot"
    COT = "chain of thought"
    POT = "programming of thought"


# 'grpcio' has been downgraded to 1.67.1 for compatibility issues (even 'grpcio-status-1.67.1')
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


def get_response(client: Client, messages, code: bool, account: str, count: int, model: str) -> str:
    res: GenerateContentResponse | None = None
    chat = client.chats.create(model=model)
    for m in messages:
        while True:
            try:
                res = chat.send_message(m)
                count = 1
            except ResourceExhausted:
                print("Resource Exhausted in " + account + " " + str(count), flush=True)
                if count == 10:
                    raise ResourceWarning("The resource in " + account + " are exhausted.")
                time.sleep(random.randint(int(pow(count, 2)) + 3, int(pow(count, 2)) + 7))
                count += 1
                continue
            except InternalServerError:
                print("Google server is not available", flush=True)
                time.sleep(30)
                continue
            except DeadlineExceeded:
                print("Deadline Exceeded - timeout reached while waiting response", flush=True)
                time.sleep(2)
                continue
            break
    if res is None:
        raise RuntimeError("No message has been found in the file.")
    #Handle code
    answer: str = res.text
    if code:
        answer = re.sub(r"```python" + "|" + r"`", "", answer)
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout
        try:
            exec(answer, dict())
            answer = re.sub("[\t\n\r\s]", "", sys.stdout.getvalue())
            sys.stdout = old_stdout
        except Exception as e:
            sys.stdout = old_stdout
            print("Gemini wrote a wrong code!\nThe following exception has raise:\n" + str(e) + "\n", flush=True)
            answer = "#"

    #Cleaning output
    out = re.sub("[|!$%&/'§#ç@;_<>?+*^ \t\n\r\s]", "", answer)
    return out + "?"


def launch_request(q_type: QuestionTypology, account: str, in_file: TextIO, client: Client,
                   message: list[dict[str, list[str]] | tuple[dict[str, list[str]], str]], model: str):
    count = 1
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    response = get_response(client, message, code, account, count, model)
    in_file.write(response)
    in_file.flush()
    #Trying to avoid Resource Exhausted error
    if q_type is QuestionTypology.OS:
        time.sleep(4)  #15 requests per minute
    elif q_type is QuestionTypology.COT:
        time.sleep(8)
    elif q_type is QuestionTypology.POT:
        time.sleep(4)
    else:
        raise ValueError("Error in QuestionTypology enum while looking for the type")


def process_main(api_key: str, q_name: str, account: str, msg_list: list[tuple[list, QuestionTypology]], iteration: int,
                 model: str):
    client = genai.Client(api_key=api_key)

    Path("..\\response\\" + model + "\\" + account + "\\" + q_name).mkdir(parents=True, exist_ok=True)
    response_file_list = list()
    for j in range(iteration):
        for msg_type_tuple in msg_list:
            response_file: TextIO
            if msg_type_tuple[1] is QuestionTypology.OS:
                response_file = open("..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "one_shot.txt",
                                     'a+')
            elif msg_type_tuple[1] is QuestionTypology.COT:
                response_file = open("..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "CoT.txt", 'a+')
            elif msg_type_tuple[1] is QuestionTypology.POT:
                response_file = open("..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "PoT.txt", 'a+')
            else:
                raise ValueError("Error in QuestionTypology enum while looking for the type")
            # one-shots require about 0.6 sec per request => 8
            # Chain of Thoughts require about 5.2 sec => 1
            # Programming of Thoughts require about 1.9 sec => 3
            launch_request(msg_type_tuple[1], account, response_file, client, msg_type_tuple[0], model)
            response_file_list.append(response_file)
        print("In " + account + ", repetition: " + str(j), flush=True)
    print(account + " done", flush=True)
    for file_c in response_file_list:
        file_c.close()


if __name__ == '__main__':
    #Constants definition
    account_api_key = [
        #HARDCODED
    ]
    #Variables definition
    file_name = "..\\questions\\"
    processes = list()
    messages_list = list()
    opt_image_path: str | None = None

    # CMD definitions and arguments parsing
    parser = argparse.ArgumentParser(
        description="This program submit multiple times the question written in the specified file to Gemini and save "
                    "the results in the 'response' folder. Actually 5 accounts are used simultaneously.",
        epilog="An example: python geminy_testing.py -q 101 -r 101")
    parser.add_argument("-q", "--question", required=True, type=int,
                        help="The question number: if the question is in the file named 'Question101', this parameter "
                             "should be 101.")
    parser.add_argument("-m", "--model", required=True, type=str,
                        choices=["gemini-2.0-flash-001", "gemini-2.0-flash-lite-001", "gemini-1.5-flash-002",
                                 "gemini-1.5-flash-8b-001", "gemini-2.0-flash-thinking-exp"],
                        help="The Gemini model to be used.")
    parser.add_argument("-r", "--repetitions", required=False, type=int,
                        help="The number of time the question will be submitted to Gemini, default: 100.", default=100)
    args = parser.parse_args()
    if 100 <= args.question < 200:
        img_path = file_name + "typology1\\img" + str(args.question) + ".png"
        file_name = file_name + "typology1\\Question" + str(args.question) + ".txt"
    elif 200 <= args.question < 300:
        img_path = file_name + "typology2\\img" + str(args.question) + ".png"
        file_name = file_name + "typology2\\Question" + str(args.question) + ".txt"
    elif 300 <= args.question < 400:
        img_path = file_name + "typology1\\img" + str(args.question) + ".png"
        file_name = file_name + "typology3\\Question" + str(args.question) + ".txt"
    else:
        raise ValueError("Error, Wrong parameters: The question number must be between 100 and 399")
    if os.path.isfile(img_path):
        opt_image_path = img_path
    file = open(file_name, "r")

    finished = False
    while not finished:
        msg = []
        question_type = get_type(file)
        finished = get_questions(file, msg, opt_image_path)
        messages_list.append((msg, question_type))
    file.close()

    question_name = re.sub(r"..\\questions\\typology" + "[0-9]" + r"\\", "", file_name).replace(".txt", "")

    for i, ak in enumerate(account_api_key):
        processes.append(Process(target=process_main, args=(
            ak, question_name, "account" + str(i), messages_list, args.repetitions, args.model
        ), name="account" + str(i)))

    for p in processes:
        p.start()
        time.sleep(1.2)
    for p in processes:
        p.join()
