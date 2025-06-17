import re
import time

import requests
from PIL.ImageFile import ImageFile
from filelock import FileLock
from huggingface_hub import InferenceClient

from src.LLMs.models_details import model_images
from src.LLMs_parameters import parameters as global_param
from src.counter_thread import CounterThread
from src.exec_generated_code_process import launch_generated_code
from src.logging_thread import LoggerInteracter
from src.structures.question_typology_class import QuestionTypology


def launch_request(q_type: QuestionTypology, account: str, in_file_path: str, message: list[str | list[ImageFile, str]],
                   model: str, logger: LoggerInteracter, counter_t: CounterThread, api_key:str):
    answer = None
    model_id = "meta-llama/"+model
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'x-use-cache' : 'false'
    }
    client = InferenceClient(
        model = model_id,
        provider = "hf-inference",
        token=api_key,
        headers=headers
    )
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    if len(message) == 0:
        raise ValueError("Trying to perform the serverless_llama/request no message has been found.")
    llm_messages = []
    for m in message:
        if model_images[model] and type(m) is list[ImageFile, str]:
            raise ValueError("TODO, not implemented yet")
            # TODO: gestione di imaagini nel prompt
        elif type(m) is str:
            llm_messages.append({
                "role": "user",
                "content": m
            })
        else:
            raise ValueError("The model doesn't support images analysis.")
        while True:
            try:
                response = client.chat.completions.create(
                    messages = llm_messages,
                    max_tokens=global_param["max_new_tokens"],
                    temperature=global_param["temperature"],
                    top_p = global_param["top_p"]
                )
                answer = str(response.choices[0].message.content)
                counter_t.count(1)
            except Exception as e:
                print(str(e))
                #TODO:gestione errori!
                time.sleep(counter_t.require_waiting_time("TIME_Unknown"))
                continue
            break
    if answer is None:
        raise ValueError("No answer has been produced.")
    if code:
        answer = launch_generated_code(answer, account)
    #Cleaning output
    out = re.sub( "[?]", "", answer)
    response = out + "?"
    response = ''.join(char for char in response if char.isascii())
    lock = FileLock(in_file_path + ".lock")
    with lock:
        in_file = open(in_file_path, 'a+')
        in_file.write(response)
        in_file.flush()
        in_file.close()
    logger.send_msg(q_type)