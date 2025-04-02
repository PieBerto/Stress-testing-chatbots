import re
import time
from multiprocessing import Process
from pathlib import Path
from time import sleep
from typing import TextIO




from google import genai

from google.genai import Client
from google.genai.errors import ServerError,ClientError
from google.genai.types import GenerateContentResponse

from src.exec_generated_code_process import exec_generated_code
from src.structures.question_typology_class import QuestionTypology


def get_response(client: Client, messages, code: bool, account: str, model: str, send_queue, receive_queue) -> str:
    res: GenerateContentResponse | None = None
    chat = client.chats.create(model=model)
    for m in messages:
        while True:
            try:
                sleep(1.5)
                res = chat.send_message(m)
                if res.text is None:
                    print(str(res))
                    continue
                send_queue.put(1)
            except ClientError as e:
                if e.code == 429:
                    #print("Resource Exhausted in " + account, flush=True)
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
                continue
            except Exception as e:
                print("Unexpected Exception error:\n" + str(e), flush=True)
                send_queue.put("TIME_Unknown")
                continue
            break
    if res is None:
        raise RuntimeError("No message has been found in the file.")
    #Handle src
    answer = res.text
    code_container = list(answer)
    if code:
        exec_p = Process(target=exec_generated_code, args=(code_container,), name =account + "_exec_generated_code")
        exec_p.start()
        exec_p.join(90)
        if exec_p.is_alive():
            exec_p.terminate()
            exec_p.join(10)
            if exec_p.is_alive():
                exec_p.kill()
            answer = "@"
        else:
            answer = code_container.pop()
        exec_p.close()
    #Cleaning output
    out = re.sub( "[?]", "", answer)
    return out + "?"


def launch_request(q_type: QuestionTypology, account: str, in_file_path: str, message: list[dict[str, list[str]] | tuple[dict[str, list[str]], str]],
                   model: str, log_msg_qq,send_queue,receive_queue, api_key:str):
    client = genai.Client(api_key=api_key)
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    response = get_response(client, message, code, account, model,send_queue, receive_queue)
    #TODO: UnicodeEncodeError: 'charmap' codec can't encode character '\u2248' in position 463: character maps to <undefined>
    response = ''.join(char for char in response if char.isascii())
    in_file = open(in_file_path, 'a+')
    in_file.write(response)
    in_file.flush()
    in_file.close()
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
