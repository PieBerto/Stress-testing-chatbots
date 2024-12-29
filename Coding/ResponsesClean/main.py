from pathlib import Path
from typing import TextIO

mini: int = 100
parent_dir = Path("..\\response")
for account in parent_dir.iterdir():
    for question in account.iterdir():
        if question.name.endswith("Question1"):
            for file in question.iterdir():
                if file.is_file():
                    f: TextIO = file.open("r")
                    stri = f.read()
                    num = stri.count(",")
                    print("in " + account.name + " in file "+ file.name + " number of answers: "+ str(num))
                    if num < mini:
                        mini = num
print(mini)