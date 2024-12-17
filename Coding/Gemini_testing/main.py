import re
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TextIO
from io import StringIO
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai import GenerativeModel

# 'grpcio' has been downgraded to 1.67.1 for compatibility issues (even 'grpcio-status-1.67.1')
#Legenda
# %% -> la domanda continua con un altra parte
# %%% -> la domanda termina ma la prossima sarà uguale con metodologia diversa: one-shot, CoT, PoT
# %%%% -> cambia la domanda
def get_questions(file_f: TextIO, messages: list[dict[str, list[str]]]):
    question = ""
    for line in file_f:
        if line == "%%\n":
            messages.append({'role': 'user','parts': [question]})
            return get_questions(file_f, messages)
        elif line == "%%%\n" or line == "%%%%\n":
            messages.append({'role': 'user','parts': [question]})
            return
        else:
            question += line

def get_response(mod: GenerativeModel, messages: list[dict[str, list[str]]], code: bool, account: str) -> str:
    new_msg_list = []
    res = ""
    for m in messages:
        new_msg_list.append(m)
        while True:
            try:
                res = mod.generate_content(new_msg_list)
            except ResourceExhausted:
                print("Resource Exhausted in "+account)
                time.sleep(30)
                continue
            break
        res.resolve()
        new_msg_list.append(res.candidates[0].content)
    res = res.text
    if code:
        res = res.replace("```python", "").replace("`", "")
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout
        try:
            exec(res)
            res = sys.stdout.getvalue().strip(' \t\n\r')
        except:
            print("Gemini wrote a wrong code!")
            res = -1
        sys.stdout = old_stdout
    # TODO check if there are different candidates!
    out = re.sub("[a-zA-Z:|!£$%&/()='§#°ç@;_<>?+*^]", "", res).strip(' \t\n\r')
    return out + ","

def launch_request(rep: int, msg_to_print: str, account: str, in_file: TextIO, mod: GenerativeModel, msg: list[dict[str, list[str]]], code: bool = False):
    for i in range(rep):
        response = get_response(mod, msg, code, account)
        print("In "+account+" launched " + msg_to_print +", repetition: " + str(i))
        in_file.write(response)
        in_file.flush()
        #Trying to avoid Resource Exhausted error
        if msg_to_print == "one-shot":
            time.sleep(2*5.5)
        elif msg_to_print == "chain of thought":
            time.sleep(2)
        elif msg_to_print == "programming of thought":
            time.sleep(2*3)
        else:
            #TODO: create an enum
            raise ValueError("If the message to print parameter has been changed, even the code must be changed")

def main(api_key: str, exe: ThreadPoolExecutor, account: str, file_name: str):
    file = open(file_name, "r")
    os_msg = []
    get_questions(file,os_msg)
    cot_msg = []
    get_questions(file,cot_msg)
    pot_msg = []
    get_questions(file,pot_msg)
    file.close()


    repetitions = 5
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    new_question_name = file_name.replace(".","").replace("\\","").replace("txt","").replace("uestion","")
    os_f = open("..\\response\\"+account+new_question_name+"_one_shot.txt",'a+')
    cot_f = open("..\\response\\"+account+new_question_name+"_CoT.txt",'a+')
    pot_f = open("..\\response\\"+account+new_question_name+"_PoT.txt",'a+')

    #one-shots require about 0.6 sec per request => 8
    future_os=exe.submit(launch_request, repetitions,"one-shot", account, os_f, model, os_msg, False)
    #Chain of Thoughts require about 5.2 sec => 1
    future_cot=exe.submit(launch_request, repetitions,"chain of thought", account,cot_f, model, cot_msg, False)
    #Programming of Thoughts require about 1.9 sec => 3
    future_pot=exe.submit(launch_request, repetitions,"programming of thought", account,pot_f, model, pot_msg, True)

    future_os.result()
    future_cot.result()
    future_pot.result()

    os_f.close()
    cot_f.close()
    pot_f.close()



exe = ThreadPoolExecutor()
file_n = "..\\_Question1.txt"
account_api_key = [
    "AIzaSyCT45sf1tGQs-ykOwAdm_G24N6tXZT6T70",
    "AIzaSyDZOeAAIEqsRu_7zGWbM5AGj5-eBUOpKBw",
    "AIzaSyCreEnPKVVRgPgZW9Jfj8OgoAz7J4VZ3CE",
    "AIzaSyAHiqh0awxJMw9BgsdDwvHYkfcsS6eu3xA"
]
futures = list()
for i,ak in enumerate(account_api_key):
    futures.append(exe.submit(main,ak, exe, "account "+str(i), file_n))
for f in futures:
    f.result()
