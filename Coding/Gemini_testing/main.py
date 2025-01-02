import random
import re
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process
from typing import TextIO
from io import StringIO
import google.generativeai as genai
from google.ai.generativelanguage_v1 import GenerateContentResponse
from google.api_core.exceptions import ResourceExhausted, InternalServerError, DeadlineExceeded
from google.generativeai import GenerativeModel
from pathlib import Path
from enum import Enum


class QuestionTypology(Enum):
    OS = "one-shot"
    COT = "chain of thought"
    POT = "programming of thought"


# 'grpcio' has been downgraded to 1.67.1 for compatibility issues (even 'grpcio-status-1.67.1')
#Legenda
# %% -> la domanda continua con un altra parte
# %%% -> la domanda termina ma la prossima sarà uguale con metodologia diversa: one-shot, CoT, PoT
# %%%% -> cambia la domanda
def get_questions(file_f: TextIO, messages: list[dict[str, list[str]]]):
    question = ""
    for line in file_f:
        if line == "%%\n":
            messages.append({'role': 'user', 'parts': [question]})
            return get_questions(file_f, messages)
        elif line == "%%%\n" or line == "%%%%\n" or line == "%%%%":
            messages.append({'role': 'user', 'parts': [question]})
            return
        else:
            question += line


def get_response(mod: GenerativeModel, messages: list[dict[str, list[str]]], code: bool, account: str, count: int) -> str:
    new_msg_list = []
    res: GenerateContentResponse
    for m in messages:
        new_msg_list.append(m)
        while True:
            try:
                res = mod.generate_content(new_msg_list)
                count=0
            except ResourceExhausted:
                print("Resource Exhausted in " + account + " " +str(count), flush=True)
                if count == 30:
                    raise ResourceWarning("The resource in " + account + " are exhausted.")
                time.sleep(random.randint(count, count+5))
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
        res.resolve()
        new_msg_list.append(res.candidates[0].content)
    answer:str = res.text
    if code:
        answer = answer.replace("```python", "").replace("`", "")
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout
        try:
            exec(answer)
            answer = sys.stdout.getvalue().replace(' ',"").replace('\t',"").replace('\n',"").replace('\r',"")
        except:
            print("Gemini wrote a wrong code!", flush=True)
            answer = ""
        sys.stdout = old_stdout
    # TODO check if there are different candidates!
    out = re.sub("[a-zA-Z:|!£$%&/()='§#°ç@;_<>?+*^ ]", "", answer).replace(' ',"").replace('\t',"").replace('\n',"").replace('\r',"")
    return out + ";"


def launch_request(msg_to_print: QuestionTypology, account: str, in_file: TextIO, mod: GenerativeModel,
                   msg: list[dict[str, list[str]]], code: bool = False):
    count = 0
    response = get_response(mod, msg, code, account, count)
    in_file.write(response)
    in_file.flush()
    #Trying to avoid Resource Exhausted error
    if msg_to_print is QuestionTypology.OS:
        time.sleep(0.2 * 5.5)
    elif msg_to_print is QuestionTypology.COT:
        time.sleep(0.2)
    elif msg_to_print is QuestionTypology.POT:
        time.sleep(0.2 * 3)
    else:
        #TODO: create an enum
        raise ValueError("Error in QuestionTypology enum while looking for the type")

def main(api_key: str, model: GenerativeModel, question_name: str, account: str, os_msg: list[dict[str, list[str]]],
         cot_msg: list[dict[str, list[str]]], pot_msg: list[dict[str, list[str]]]):
    #NUMBER OF REPETITIONS! <---------------------------------------------------------------------------------------------
    repetitions = 100
    genai.configure(api_key=api_key)

    Path("..\\response\\Gemini-1.5-flash\\" + account + "\\" + question_name).mkdir(parents=True, exist_ok=True)
    os_f = open("..\\response\\Gemini-1.5-flash\\" + account + "\\" + question_name + "\\" + "one_shot.txt", 'a+')
    cot_f = open("..\\response\\Gemini-1.5-flash\\" + account + "\\" + question_name + "\\" + "CoT.txt", 'a+')
    pot_f = open("..\\response\\Gemini-1.5-flash\\" + account + "\\" + question_name + "\\" + "PoT.txt", 'a+')
    for i in range(repetitions):
        #one-shots require about 0.6 sec per request => 8
        launch_request(QuestionTypology.OS, account, os_f, model, os_msg, False)
        #Chain of Thoughts require about 5.2 sec => 1
        launch_request(QuestionTypology.COT, account, cot_f, model, cot_msg, False)
        #Programming of Thoughts require about 1.9 sec => 3
        launch_request(QuestionTypology.POT, account, pot_f, model, pot_msg, True)
        print("In " + account + ", repetition: " + str(i), flush=True)
    print(account + " done", flush=True)
    os_f.close()
    cot_f.close()
    pot_f.close()


if __name__ == '__main__':
    account_api_key = [
        "AIzaSyCT45sf1tGQs-ykOwAdm_G24N6tXZT6T70",
        "AIzaSyDZOeAAIEqsRu_7zGWbM5AGj5-eBUOpKBw",
        "AIzaSyCreEnPKVVRgPgZW9Jfj8OgoAz7J4VZ3CE",
        "AIzaSyAHiqh0awxJMw9BgsdDwvHYkfcsS6eu3xA",
        "AIzaSyCMqg3JSPUqQq4WHAIrsMQOKichZS-WKxk",
        "AIzaSyBXZcf_W2y_OShJ7otGKQThR0VCO4FvTp0"
    ]

    file_name = "..\\questions\\typology1\\Question3.txt"
    file = open(file_name, "r")
    one_shot_msg = []
    get_questions(file, one_shot_msg)
    chain_of_thoughts_msg = []
    get_questions(file, chain_of_thoughts_msg)
    programming_of_thoughts_msg = []
    get_questions(file, programming_of_thoughts_msg)
    file.close()

    model = genai.GenerativeModel("gemini-1.5-flash")

    question_name = file_name.replace("..\\questions\\typology1\\", "").replace(".txt", "")

    processes = list()
    for i, ak in enumerate(account_api_key):
        processes.append(Process(target=main, args=(
            ak, model, question_name, "account" + str(i), one_shot_msg, chain_of_thoughts_msg,
            programming_of_thoughts_msg), name="account" + str(i)))
    for p in processes:
        p.start()
        time.sleep(2.5)
    for p in processes:
        p.join()
