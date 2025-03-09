import os
import random
import argparse
import re
import sys
import threading
import time
from datetime import datetime
from google.genai import Client
from multiprocessing import Process
from queue import Queue
from typing import TextIO
from io import StringIO
from google import genai
from google.ai.generativelanguage_v1 import GenerateContentResponse
from google.api_core.exceptions import ResourceExhausted, InternalServerError, DeadlineExceeded
from pathlib import Path
from enum import Enum
import PIL.Image
from google.genai.errors import ServerError


#TODO: Se non riesco ad eseguire il codice di gemini non devo aggiungerlo al file di log. Il file di log deve determinare quante iterazioni fare (forse)
#python .\gemini_testing.py -q 106 -r 1 -m gemini-2.0-flash-001 -k C:\Users\pietr\Desktop\Gemini_API_key.txt

class QuestionTypology(Enum):
    OS = "one-shot"
    COT = "chain of thought"
    POT = "programming of thought"


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
    print(lines)
    file.writelines(lines)
    file.flush()


def logging(question_name: str, log_file_name: str, log_msg_qq: Queue):
    while True:
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
                    break
        except Exception as e:
            print("Exception occurred while writing the log file:\n", str(e))
            log_file.truncate(0)
            log_file.writelines(backup)
            log_file.flush()
        log_file.close()


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
            except ServerError as e:
                print("Server error:\n" + str(e) + "\n", flush=True)
                time.sleep(30)
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
                   message: list[dict[str, list[str]] | tuple[dict[str, list[str]], str]], model: str, log_msg_qq: Queue,):
    count = 1
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    response = get_response(client, message, code, account, count, model)
    in_file.write(response)
    in_file.flush()
    log_msg_qq.put(q_type)
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
    #Logging process start
    log_file_name = "C:\\GitHub\\Stress-testing-chatbots\\Coding\\response\\gemini-2.0-flash-001\\"+ account +"\\response_log.txt"
    log_msg_qq = Queue()
    if not os.path.isfile(log_file_name):
        log_file = open(log_file_name, "x")
        log_file.write(
            "This file explains when the tests were carried out, the dates are expressed: [year-month-day].\n\n")
        log_file.flush()
        log_file.close()
    logging_thread = threading.Thread(target = logging, args = [q_name.replace(".txt",""),log_file_name,log_msg_qq], name = account+"_logging")
    logging_thread.start()

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
            launch_request(msg_type_tuple[1], account, response_file, client, msg_type_tuple[0], model, log_msg_qq)
            response_file_list.append(response_file)
        print("In " + account + ", repetition: " + str(j), flush=True)
    print(account + " done", flush=True)
    for file_c in response_file_list:
        file_c.close()

    log_msg_qq.put("TERMINATE")
    logging_thread.join()


def command_line_args():
    file_name = "..\\questions\\"
    opt_image_path: str | None = None
    parser = argparse.ArgumentParser(
        description="This program submit multiple times the question written in the specified file to Gemini and save "
                    "the results in the 'response' folder.",
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
    parser.add_argument("-k", "--api_key_file", required=True, type=str,
                        help="The path to the file containing the API key.")
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
    if not os.path.isfile(file_name):
        raise ValueError("Error, Question File '" + file_name + "' does not exist")
    if os.path.isfile(img_path):
        opt_image_path = img_path
    file = open(file_name, "r")
    if not os.path.isfile(args.api_key_file):
        raise ValueError("Error, API_key File '" + args.api_key_file + "' does not exist")
    # Retrieving the api_keys from the file
    api_key_file = open(args.api_key_file, "r")
    account_api_key = list()
    for line in api_key_file:
        if not line.startswith("#"):
            account_api_key.append(line.replace("\"", "").strip())
    print("Number of api_keys: " + str(len(account_api_key)), flush=True)
    return file_name, file, opt_image_path, account_api_key, args.repetitions, args.model


def main():
    (file_name, file, opt_image_path, account_api_key, repetitions, model) = command_line_args()

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
    for i, ak in enumerate(account_api_key):
        processes.append(Process(target=process_main, args=(
            ak, question_name, "account" + str(i), messages_list, repetitions, model
        ), name="account" + str(i)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
