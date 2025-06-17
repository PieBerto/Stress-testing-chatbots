import re
import time
from time import sleep

from PIL.ImageFile import ImageFile
from filelock import FileLock
from google import genai
from google.genai import Client
from google.genai.errors import ServerError, ClientError
from google.genai.types import GenerateContentResponse, GenerateContentConfig

from src.LLMs_parameters import parameters as global_param
from src.counter_thread import CounterThread
from src.exec_generated_code_process import launch_generated_code
from src.logging_thread import LoggerInteracter
from src.structures.question_typology_class import QuestionTypology


def get_response(client: Client, messages, code: bool, account: str, model: str, counter_t: CounterThread) -> str:
    config = GenerateContentConfig(
        max_output_tokens=global_param["max_new_tokens"],
        temperature=global_param["temperature"],
        top_p=global_param["top_p"],
        top_k=global_param["top_k"])
    res: GenerateContentResponse | None = None
    chat = client.chats.create(model = model, config = config)
    for m in messages:
        while True:
            try:
                sleep(1.5)
                res = chat.send_message(m)
                if res.text is None:
                    print("No text in response, the response is:\n"+str(res))
                    continue
                counter_t.count(1)
            except ClientError as e:
                if e.code == 429:
                    #print("Resource Exhausted in " + account +"\n"+str(e), flush=True)
                    time.sleep(counter_t.require_waiting_time("TIME_ResourceExhausted"))
                else:
                    print("Unexpected ClientError error:\n" + str(e), flush=True)
                    time.sleep(counter_t.require_waiting_time("TIME_Unknown"))
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
                time.sleep(counter_t.require_waiting_time("TIME_ServerError"))
                continue
            except Exception as e:
                print("Unexpected general Exception:\n" + str(e), flush=True)
                time.sleep(counter_t.require_waiting_time("TIME_Unknown"))
                continue
            break
    if res is None:
        raise RuntimeError("No message has been found in the file.")
    #Handle src
    answer = res.text
    if code:
        answer = launch_generated_code(answer, account)
    #Cleaning output
    out = re.sub( "[?]", "", answer)
    return out + "?"


def launch_request(q_type: QuestionTypology, account: str, in_file_path: str, message: list[str | list[ImageFile, str]],
                   model: str, logger: LoggerInteracter, counter_t: CounterThread, api_key:str):
    client = genai.Client(api_key=api_key)
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    response = get_response(client, message, code, account, model,counter_t)
    response = ''.join(char for char in response if char.isascii())
    lock = FileLock(in_file_path+".lock")
    with lock:
        in_file = open(in_file_path, 'a+')
        in_file.write(response)
        in_file.flush()
        in_file.close()
    logger.send_msg(q_type)
    #Trying to avoid Resource Exhausted error
    #if q_type is QuestionTypology.OS:
    #    time.sleep(4)  #15 requests per minute
    #elif q_type is QuestionTypology.COT:
    #    time.sleep(8)
    #elif q_type is QuestionTypology.POT:
    #    time.sleep(4)
    #else:
    #    raise ValueError("Error in QuestionTypology enum while looking for the type")
