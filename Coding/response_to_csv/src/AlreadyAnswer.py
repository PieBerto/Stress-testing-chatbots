import json
import os
from pathlib import Path

from filelock import FileLock


class AlreadyAnswer:
    content:dict = {}
    def __init__(self, file_path):
        parent_folder = Path(str(file_path).removesuffix(str(os.path.basename(file_path))))
        if not parent_folder.exists():
            parent_folder.mkdir(parents=True, exist_ok=False)
        lock = FileLock(str(file_path) + ".lock")
        lock.acquire()
        if not file_path.is_file():
            my_file = open(file_path, "x")
            my_file.write("{}")
        else:
            my_file = open(file_path, "r")
            self.content = json.load(my_file)
        my_file.close()
        lock.release()
        self.file_path = file_path

    def _add_answer(self, question:str, answer:str, interpreted_answer:str):
        if question not in self.content.keys():
            self.content[question] = list()
        self.content[question].append( {
            "answer": answer,
            "interpreted_answer": interpreted_answer
        })
        lock = FileLock(str(self.file_path) + ".lock")
        lock.acquire()
        with open(self.file_path, "w") as file:
            json.dump(self.content, file)
        lock.release()

    def search_answer(self, question:str, answer:str) -> str:
        interpreted_answer = None
        if question in self.content.keys():
            for answer_dict in self.content[question]:
                if answer_dict["answer"] == answer:
                    interpreted_answer =  answer_dict["interpreted_answer"]
        if interpreted_answer is None:
            print(answer)
            if question == "q104":
                message = "Question "+question+", replace the previous coordinates in the form 'X,Y', without quotes:\t"
            else:
                message = "Question " + question + ", replace the previous entry:\t"
            interpreted_answer = input(
                message).strip(" \n\t\r")
            print("\n---------------------\n")
            if interpreted_answer == "":
                interpreted_answer = "+"
            self._add_answer(question, answer, interpreted_answer)
        return interpreted_answer