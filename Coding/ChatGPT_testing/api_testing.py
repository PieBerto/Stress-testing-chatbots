import random
import re
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process
from typing import TextIO
from io import StringIO
from openai import OpenAI, RateLimitError
from pathlib import Path
from enum import Enum

from openai.types.chat.chat_completion import Choice


class QuestionTypology(Enum):
    OS = "one-shot"
    COT = "chain of thought"
    POT = "programming of thought"


# TODO: DON'T WORK, MUST PAY TO USE AN API_KEY
#Legenda
# %% -> la domanda continua con un altra parte
# %%% -> la domanda termina ma la prossima sarà uguale con metodologia diversa: one-shot, CoT, PoT
# %%%% -> cambia la domanda
def get_questions(file_f: TextIO, messages: list[dict[str, list[str]]]):
    question = ""
    for line in file_f:
        if line == "%%\n":
            messages.append({'role': 'user', 'content': [question]})
            return get_questions(file_f, messages)
        elif line == "%%%\n" or line == "%%%%\n" or line == "%%%%":
            messages.append({'role': 'user', 'content': [question]})
            return
        else:
            question += line


def get_response(client: OpenAI, messages: list[dict[str, list[str]]], code: bool, account: str, count: int) -> str:
    new_msg_list = []
    res: Choice
    for m in messages:
        new_msg_list.append(m)
        while True:
            try:
                completion = client.chat.completions.create(
                    model = "gpt-4o-mini-2024-07-18",
                    messages = new_msg_list,
                )
                res = completion.choices[0].message
                count=0
            except RateLimitError:
                print("Resource Exhausted in " + account + " " +str(count), flush=True)
                if count == 25:
                    raise ResourceWarning("The resource in " + account + " are exhausted.")
                time.sleep(random.randint(int(count*1.5)+3, int(count*1.5)+8))
                count += 1
                continue
            #except InternalServerError:
             #   print("Google server is not available", flush=True)
              #  time.sleep(30)
               # continue
            #except DeadlineExceeded:
             #   print("Deadline Exceeded - timeout reached while waiting response", flush=True)
              #  time.sleep(2)
               # continue
            break
        new_msg_list.append(res)
    answer:str = res.content
    if code:
        print(answer)
        answer = answer.replace("```python", "").replace("`", "")
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout
        try:
            exec(answer)
            answer = sys.stdout.getvalue().replace(' ',"").replace('\t',"").replace('\n',"").replace('\r',"")
        except:
            print("ChatGPT wrote a wrong code!", flush=True)
            answer = ""
        sys.stdout = old_stdout
    # TODO check if there are different candidates!
    out = re.sub("[a-zA-Z:|!£$%&/()='§#°ç@;_<>?+*^ ]", "", answer).replace(' ',"").replace('\t',"").replace('\n',"").replace('\r',"")
    return out + ";"


def launch_request(msg_to_print: QuestionTypology, account: str, in_file: TextIO, client: OpenAI,
                   msg: list[dict[str, list[str]]], code: bool = False):
    count = 0
    response = get_response(client, msg, code, account, count)
    in_file.write(response)
    in_file.flush()
    #Trying to avoid Resource Exhausted error
    if msg_to_print is QuestionTypology.OS:
        time.sleep(20)
    elif msg_to_print is QuestionTypology.COT:
        time.sleep(40)
    elif msg_to_print is QuestionTypology.POT:
        time.sleep(20)
    else:
        raise ValueError("Error in QuestionTypology enum while looking for the type")

def main(api_key: str, question_name: str, account: str, os_msg: list[dict[str, list[str]]],
         cot_msg: list[dict[str, list[str]]], pot_msg: list[dict[str, list[str]]]):
    #NUMBER OF REPETITIONS! <---------------------------------------------------------------------------------------------
    repetitions = 100
    client = OpenAI(api_key = api_key)

    Path("..\\response\\gpt-4o-mini-2024-07-18\\" + account + "\\" + question_name).mkdir(parents=True, exist_ok=True)
    os_f = open("..\\response\\gpt-4o-mini-2024-07-18\\" + account + "\\" + question_name + "\\" + "one_shot.txt", 'a+')
    cot_f = open("..\\response\\gpt-4o-mini-2024-07-18\\" + account + "\\" + question_name + "\\" + "CoT.txt", 'a+')
    pot_f = open("..\\response\\gpt-4o-mini-2024-07-18\\" + account + "\\" + question_name + "\\" + "PoT.txt", 'a+')
    for i in range(repetitions):
        #one-shots require about 0.6 sec per request => 8
        launch_request(QuestionTypology.OS, account, os_f, client, os_msg, False)
        #Chain of Thoughts require about 5.2 sec => 1
        launch_request(QuestionTypology.COT, account, cot_f, client, cot_msg, False)
        #Programming of Thoughts require about 1.9 sec => 3
        launch_request(QuestionTypology.POT, account, pot_f, client, pot_msg, True)
        print("In " + account + ", repetition: " + str(i), flush=True)
    print(account + " done", flush=True)
    os_f.close()
    cot_f.close()
    pot_f.close()


if __name__ == '__main__':
    account_api_key = [
        "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"
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



    question_name = file_name.replace("..\\questions\\typology1\\", "").replace(".txt", "")

    processes = list()
    for i, ak in enumerate(account_api_key):
        processes.append(Process(target=main, args=(
            ak, question_name, "account" + str(i), one_shot_msg, chain_of_thoughts_msg,
            programming_of_thoughts_msg), name="account" + str(i)))
    for p in processes:
        p.start()
        time.sleep(2.5)
    for p in processes:
        p.join()
