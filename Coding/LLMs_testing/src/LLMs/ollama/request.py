import base64
import re
import time
from pathlib import Path

import ollama
from PIL.ImageFile import ImageFile
from filelock import FileLock
from ollama import ResponseError

from src.LLMs.models_details import model_images, ollama_models
from src.LLMs_parameters import parameters
from src.counter_thread import CounterThread
from src.exec_generated_code_process import launch_generated_code
from src.logging_thread import LoggerInteracter
from src.structures.question_typology_class import QuestionTypology

def ollama_create(model: str):
    my_model = "my_" + model
    if model.replace("_", ":") in ollama_models:
        try:
            ollama.delete(my_model)
        except Exception as e:
            print("Error while deleting ollama model:\n", e)
        ollama.create(model=my_model, from_=model.replace("_", ":"),
                      system="Answer always using less then " + str(parameters["max_new_tokens"]) + " tokens.",
                      parameters={
                          "temperature": parameters["temperature"],
                          "top_k": parameters["top_k"],
                          "top_p": parameters["top_p"],
                          "num_ctx": parameters["max_new_tokens"],
                      })

def launch_request(q_type: QuestionTypology, account: str, in_file_path: str, message: list[str | list[ImageFile, str]],
                   model: str, logger: LoggerInteracter, counter_t: CounterThread, my_model: str):
    answer = None
    code = False
    if q_type is QuestionTypology.POT:
        code = True
    if len(message) == 0:
        raise ValueError("Trying to perform the serverless_llama/request no message has been found.")
    llm_messages = []
    for m in message:
        if model_images[model] and type(m) is list[ImageFile, str]:
            msg = m.pop()
            tmp_img: ImageFile = m.pop()
            img = base64.b64encode(Path(tmp_img.filename).read_bytes()).decode()
            llm_messages.append({
                "role": "user",
                "content": msg,
                "images": img,
            })
        elif type(m) is str:
            llm_messages.append({
                "role": "user",
                "content": m
            })
        else:
            msg = m.pop()
            tmp_img: ImageFile = m.pop()
            img = base64.b64encode(Path(tmp_img.filename).read_bytes()).decode()
            image_description = ollama.chat(
                model = "llava:7b",
                messages = [{"role": "user", "content": "Describe the image so that another another LLM can understand the content, be very detailed and report all written information in an orderly manner","images": img}],
            )
            llm_messages.append({
                "role":"system",
                "content": "Here follow the description of the image that will be used in the next user's question:\n\n"+image_description.message.content,
            })
            llm_messages.append({
                "role": "user",
                "content": msg,
            })
        while True:
            try:
                stream = ollama.chat(
                    model = my_model,
                    messages=llm_messages,
                    stream = True,
                )
                response = ""
                for i,chunk in enumerate(stream):
                    response += chunk.message.content
                    if i >= parameters["max_new_tokens"]+20:
                        print("ended")
                        break
                answer = response
                counter_t.count(1)
            except ResponseError as e:
                ollama_create(model)
                continue
            except Exception as e:
                # TODO:gestione errori!
                time.sleep(counter_t.require_waiting_time("TIME_Unknown"))
                continue
            break
        llm_messages.append({
            "role": "assistant",
            "content": answer,
        })
    if answer is None:
        raise ValueError("No answer has been produced.")
    if code:
        answer = launch_generated_code(answer, account)
    # Cleaning output
    out = re.sub("[?]", "", answer)
    response = out + "?"
    response = ''.join(char for char in response if char.isascii())
    lock = FileLock(in_file_path + ".lock")
    with lock:
        in_file = open(in_file_path, 'a+')
        in_file.write(response)
        in_file.flush()
        in_file.close()
    logger.send_msg(q_type)