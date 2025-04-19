import multiprocessing
import queue
import re
from contextlib import redirect_stdout
from io import StringIO
from multiprocessing import Process



def exec_generated_code(my_queue: multiprocessing.Queue, code: str):
    answer = re.sub(r"```python" + "|" + r"`", "", code)
    try:
        out = StringIO()
        with redirect_stdout(out):
            exec(answer,dict())
        solution = re.sub("[#@?]", "", out.getvalue())
    except Exception as e:
        print("The LLM wrote a wrong src, the following exception has raise:\n" + str(e) + "\n", flush=True)
        solution = "#"
    my_queue.put(solution)


def launch_generated_code(answer: str, account: str) -> str:
    my_queue = multiprocessing.Queue()
    exec_p = Process(target=exec_generated_code, args=(my_queue,answer), name =account + "_exec_generated_code")
    exec_p.start()
    try:
        new_answer = my_queue.get(timeout=78.0)
    except queue.Empty:
        new_answer = "@"
        print("In PoT the execution of the code timeout, no code produced.", flush=True)
    exec_p.join(timeout=2.0)
    if exec_p.is_alive():
        exec_p.terminate()
        exec_p.join(10)
        if exec_p.is_alive():
            exec_p.kill()
        print("exec killed.",flush=True)
    exec_p.close()
    return new_answer