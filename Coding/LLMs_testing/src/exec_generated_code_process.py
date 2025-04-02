import re
import sys
from io import StringIO

def exec_generated_code(code_container: list[str]):
    code = code_container.pop()
    answer = re.sub(r"```python" + "|" + r"`", "", code)
    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout
    try:

        exec(answer, dict())
        answer = re.sub("[#@?]", "", sys.stdout.getvalue())
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        print("Gemini wrote a wrong src!\nThe following exception has raise:\n" + str(e) + "\n", flush=True)
        answer = "#"
    code_container.append(answer)