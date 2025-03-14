import re
import sys
import threading
import time
from io import StringIO
from multiprocessing import Queue as MultiQueue
from queue import Queue
from time import sleep
from typing import TextIO

from google import genai
from google.ai.generativelanguage_v1 import GenerateContentResponse
from google.genai import Client
from google.genai.errors import ServerError,ClientError

from sample.counter_process_thread import counter
from sample.structures.question_typology_class import QuestionTypology

#TODO: 0- trova gli errori generati da Gemini, poco alla volta quando sorgono poi gestiscili
def get_response(client: Client, messages, code: bool, account: str, model: str, send_queue, receive_queue) -> str:
    res: GenerateContentResponse | None = None
    chat = client.chats.create(model=model)
    for m in messages:
        while True:
            try:
                sleep(1.5)
                res = chat.send_message(m)
                send_queue.put(1)
            except ClientError as e:
                if e.code == 429:
                    print("Resource Exhausted in " + account, flush=True)
                    send_queue.put("TIME_ResourceExhausted")
                    w_time = float(receive_queue.get())
                    time.sleep(w_time)
                else:
                    print("Unexpected ClientError error:\n" + str(e), flush=True)
                    send_queue.put("TIME_Unknown")
                continue
            #except InternalServerError:
            #    print("Google server is not available", flush=True)
            #    send_queue.put("TIME_InternalServerError")
            #    w_time = float(receive_queue.get())
            #    time.sleep(w_time)
            #    continue
            #except DeadlineExceeded:
            #    print("Deadline Exceeded - timeout reached while waiting response", flush=True)
            #    send_queue.put("TIME_DeadlineExceeded")
            #    time.sleep(2)
            #    continue
            except ServerError as e:
                print("Server error:\n" + str(e) + "\n", flush=True)
                send_queue.put("TIME_ServerError")
                w_time = float(receive_queue.get())
                time.sleep(w_time)
            except Exception as e:
                print("Unexpected Exception error:\n" + str(e), flush=True)
                send_queue.put("TIME_Unknown")
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
                   message: list[dict[str, list[str]] | tuple[dict[str, list[str]], str]], model: str, log_msg_qq: MultiQueue,send_queue,receive_queue):
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    response = get_response(client, message, code, account, model,send_queue, receive_queue)
    in_file.write(response)
    in_file.flush()
    log_msg_qq.put(q_type)
    #Trying to avoid Resource Exhausted error
    #if q_type is QuestionTypology.OS:
    #    time.sleep(4)  #15 requests per minute
    #elif q_type is QuestionTypology.COT:
    #    time.sleep(8)
    #elif q_type is QuestionTypology.POT:
    #    time.sleep(4)
    #else:
    #    raise ValueError("Error in QuestionTypology enum while looking for the type")



def process_main(api_key: str, q_name: str, account: str, msg_list: list[tuple[list, QuestionTypology]], iteration: int,
                 model: str, log_msg_qq: MultiQueue):
    client = genai.Client(api_key=api_key)

    send_request_count_queue = Queue()
    receive_request_count_queue = Queue()
    counter_t = threading.Thread(target=counter,args=[send_request_count_queue,receive_request_count_queue, model, account],name=account+"request_count")
    counter_t.start()

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
            launch_request(msg_type_tuple[1], account, response_file, client, msg_type_tuple[0], model, log_msg_qq, send_request_count_queue, receive_request_count_queue)
            response_file_list.append(response_file)
        print("In " + account + ", repetition: " + str(j), flush=True)
    print(account + " done", flush=True)
    for file_c in response_file_list:
        file_c.close()

    log_msg_qq.put("TERMINATE")

    send_request_count_queue.put("TERMINATE")
    counter_t.join()
    print("Counter joined in account " + account + ".")