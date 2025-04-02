import time
from queue import Queue

from src.LLMs.models_details import model_to_limits


def wait_fx(start_time,count: int) -> float:
    if count >= 10:
        count = 10
    return ((start_time-time.time())%60)+3*count

def counter(receive_queue: Queue, send_queue: Queue, model: str, account: str):
    count_request = 0
    start_time = time.time()
    sequence_error = 0
    msg = "start"
    while msg != "TERMINATE":
        msg = receive_queue.get()
        if type(msg) == int:
            sequence_error = 0
            count_request += msg
        elif type(msg) == str:
            if msg == "TERMINATE":
                break
            elif str(msg).startswith("TIME_"):
                sequence_error += 1
                error = str(msg).replace("TIME_","")
                if error == "ResourceExhausted":
                    if count_request >= model_to_limits[model][1]-1 or sequence_error >= 10:
                        raise ResourceWarning("The resource in " + account + " are exhausted.")
                    duration = wait_fx(start_time,sequence_error)
                    send_queue.put(duration)
                elif error == "InternalServerError" or error == "ServerError":
                    send_queue.put(30.0)
                elif error == "DeadlineExceeded":
                    send_queue.put(30.0)
                elif error == "Unknown":
                    send_queue.put(62.0)
                else:
                    raise ValueError("The counter thread has received an ERROR that can't be recognized, check the spelling. msg: " + msg)
            else:
                raise ValueError("The counter thread has received a wrong message. msg: " + msg)
        else:
            raise ValueError("The counter thread has received a wrong message. msg: " + msg)