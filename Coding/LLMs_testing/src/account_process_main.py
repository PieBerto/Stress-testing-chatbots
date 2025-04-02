import threading
from pathlib import Path
from queue import Queue
from typing import TextIO

from src.LLMs.Gemini.request import launch_request as gemini_launch_request
from src.LLMs.models_details import gemini_models
from src.counter_thread import counter
from src.structures.question_typology_class import QuestionTypology


def process_main(api_key: str, q_name: str, account: str, msg_list: list[tuple[list, QuestionTypology]], iteration: int,
                 model: str, log_msg_qq):

    send_request_count_queue = Queue()
    receive_request_count_queue = Queue()
    counter_t = threading.Thread(target=counter,args=[send_request_count_queue,receive_request_count_queue, model, account],name=account+"request_count")
    counter_t.start()

    for j in range(iteration):
        for msg_type_tuple in msg_list:
            file_path: str
            if msg_type_tuple[1] is QuestionTypology.OS:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "one_shot.txt"
            elif msg_type_tuple[1] is QuestionTypology.COT:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "CoT.txt"
            elif msg_type_tuple[1] is QuestionTypology.POT:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "PoT.txt"
            else:
                raise ValueError("Error in QuestionTypology enum while looking for the type")
            # one-shots require about 0.6 sec per request => 8
            # Chain of Thoughts require about 5.2 sec => 1
            # Programming of Thoughts require about 1.9 sec => 3
            if model in gemini_models:
                gemini_launch_request(msg_type_tuple[1], account, file_path, msg_type_tuple[0], model, log_msg_qq, send_request_count_queue, receive_request_count_queue, api_key)
            else:
                raise ValueError("Can't find the specified model")

        print("In " + account + ", repetition: " + str(j), flush=True)
    print(account + " done", flush=True)

    log_msg_qq.put("TERMINATE")

    send_request_count_queue.put("TERMINATE")
    counter_t.join()