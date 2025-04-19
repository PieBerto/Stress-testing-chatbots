import threading
import time
from queue import Queue

from src.LLMs.models_details import model_to_limits

class CounterThread:
    def __init__(self, model, account):
        self.receiver = Queue()
        self.sender = Queue()
        self.model = model
        self.account = account
        self.count_request = 0
        self.thread = threading.Thread(target=self.__counter,
                         name=self.account + "request_count")


    @staticmethod
    def __wait_fx(start_time,count: int) -> float:
        if count <= 0:
            count = 1
        if count >= 70:
            count = 71
        base_wait = ((start_time-time.time())%60) + 1
        if count <= 5:
            return base_wait+3
        elif count <= 10:
            return base_wait+5
        elif count <= 20:
            return base_wait+20
        elif count <= 30:
            return base_wait+30
        elif count <= 40:
            return base_wait+45
        elif count <= 50:
            return base_wait+60
        elif count <= 60:
            return base_wait+90
        elif count <= 70:
            return base_wait+120
        return base_wait + 300

    def __counter(self):
        (receive_queue,send_queue,model,account) = (self.receiver, self.sender, self.model, self.account)

        start_time = time.time()
        sequence_error = 0
        msg = "start"
        while msg != "TERMINATE":
            msg = receive_queue.get()
            if type(msg) == int:
                sequence_error = 0
                self.count_request += msg
            elif type(msg) == str:
                if msg == "TERMINATE":
                    break
                elif str(msg).startswith("TIME_"):
                    sequence_error += 1
                    error = str(msg).replace("TIME_","")
                    if error == "ResourceExhausted":
                        if sequence_error == 71: #or self.count_request >= model_to_limits[model][1]-1:
                            print("The resource in " + account + " are exhausted.")
                        duration = self.__wait_fx(start_time, sequence_error)
                        send_queue.put(duration)
                    elif error == "InternalServerError" or error == "ServerError":
                        send_queue.put(30.0)
                    elif error == "DeadlineExceeded":
                        send_queue.put(30.0)
                    elif error == "Unknown":
                        send_queue.put(30.0)
                    else:
                        raise ValueError("The counter thread has received an ERROR that can't be recognized, check the spelling. msg: " + msg)
                else:
                    raise ValueError("The counter thread has received a wrong message. msg: " + msg)
            else:
                raise ValueError("The counter thread has received a wrong message. msg: " + msg)

    def require_waiting_time(self,error_name: str) -> float:
        (sender,receiver) = (self.receiver, self.sender)
        sender.put(error_name)
        w_time = float(receiver.get())
        return w_time

    def start(self):
        self.thread.start()

    def join(self):
        (sender, receiver) = (self.receiver, self.sender)
        sender.put("TERMINATE")
        self.thread.join()

    def count(self,times: int):
        (sender, receiver) = (self.receiver, self.sender)
        sender.put(times)