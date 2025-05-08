import math
import os
import re
import string
from operator import truediv
from pathlib import Path
from typing import TextIO

from src.AlreadyAnswer import AlreadyAnswer
from src.file_and_lock import read_file, write_entry

questions = {}
remember = AlreadyAnswer(Path(r"C:\GitHub\Stress-testing-chatbots\Coding\csv\support_file\already_answered.json"))

def insert_fx(fx, params):
    global questions
    if questions.get("q101") is None:
        questions["q101"] = list()
    questions["q101"].append((fx,params))

def question_select(filename: Path, out_file: Path, model:str, account:str):
    folder_name = filename.stem
    match folder_name:
        case "Question101":
            #iterate(filename,out_file,q101, model, account)
            pass
        case "Question102":
            #iterate(filename,out_file,q102, model, account)
            pass
        case "Question103":
            #iterate(filename,out_file, q103, model, account)
            pass
        case "Question104":
            #iterate(filename,out_file, q104, model, account)
            pass
        case "Question105":
            #iterate(filename,out_file, q105, model, account)
            pass
        case "Question106":
            iterate(filename,out_file, q106, model, account)
            pass
        case "Question201":
            #iterate(filename,out_file, q201, model, account)
            pass
        case "Question202":
            #iterate(filename,out_file, q202, model, account)
            pass
        case "Question203":
            #iterate(filename,out_file, q203, model, account)
            pass
        case "Question204":
            #iterate(filename,out_file, q204, model, account)
            pass
        case "Question205":
            # iterate(filename,out_file, q205, model, account)
            pass
        case "Question206":
            # iterate(filename,out_file, q205, model, account)
            pass
        case "Question301":
            #iterate(filename,out_file, q301, model, account)
            pass
        case "Question302":
            #iterate(filename,out_file, q302, model, account)
            pass
        case "Question303":
            #iterate(filename,out_file, q303, model, account)
            pass
        case "Question304":
            #iterate(filename,out_file, q304, model, account)
            pass
        case "Question305":
            #iterate(filename,out_file, q305, model, account)
            pass
        case "Question306":
            #iterate(filename,out_file, q306, model, account)
            pass
        case "Question307":
            #iterate(filename,out_file, q307, model, account)
            pass
        case "Question308":
            #iterate(filename,out_file, q308, model, account)
            pass
        case "Question309":
            #iterate(filename,out_file, q309, model, account)
            pass
        case "Question310":
            #iterate(filename,out_file, q310, model, account)
            pass
        case _:
            raise ValueError("folder name: " + folder_name + " has not been recognized.")


def iterate(path: Path, out_file:Path, fx, model:str, account:str):
    for path, folders, files in os.walk(path):
        for file_name in files:
            if file_name == "one_shot.txt" or file_name == "CoT.txt" or file_name == "PoT.txt":
                print("\t\t\t"+file_name)
                content: list[str] = read_file(Path(os.path.join(path, file_name))).strip().split("?")
                global questions
                insert_fx(fx,(content,out_file,model,account,file_name.replace(".txt", "")))

def q101(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        extra_entry = None
        new_entry = entry.replace(" ","").replace("\n", "").replace("\r", "").replace("\t", "").replace(",","")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
                    new_entry = int (new_entry)
            except:
                if model == "gemini-2.0-flash-thinking-exp":
                    x = re.findall(r"boxed\{"+r"(\d)"+r"\}",entry)
                    if len(x) == 0:
                        x = re.findall("[Ff]inal"+' '+"*"+"[Aa]nswer:"+' '+"*"+r"(\d)", entry)
                        if len(x) == 0:
                            x = re.findall("[Ss]olution:"+' '+"*"+r"(\d)", entry)
                            if len(x) == 0:
                                x = re.findall("[Aa][Nn][Ss][Ww][Ee][Rr]:"+' '+"*"+r"(\d)", entry)
                    try:
                        (answer) = x.pop()
                        extra_entry = int(answer)
                    except Exception as e:
                        extra_entry = remember.search_answer("q101",entry)
                else:
                    new_entry = remember.search_answer("q101",entry)
            if extra_entry is not None:
                new_entry = extra_entry
            write_entry(Path(os.path.join(out_path,"q101"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q102(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    i = 0
    for entry in entries:
        i += 1
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("$","").replace("€","").replace(",","")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
            except Exception as e:
                new_entry = remember.search_answer("q102",entry)
            finally:
                write_entry(Path(os.path.join(out_path,"q102"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q103(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("$","").replace("€","").replace(",","")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
            except:
                new_entry = remember.search_answer("q103",entry)
            write_entry(Path(os.path.join(out_path,"q103"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q104(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,x,y\n"
    r = re.compile(r"^\d*[.]?\d*$")
    for entry in entries:
        new_entry = entry.lower().replace("final answer:","").replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("(","").replace(")","")
        if new_entry != "":
            if new_entry != "@" and new_entry != "#":
                if r.match(new_entry):
                    new_entry = "+"
                else:
                    c_list = new_entry.split(",")
                    try:
                        x = float(c_list[0])
                        y = float(c_list[1])
                        new_entry = str(x) + "," + str(y)
                    except:
                        if model == "gemini-2.0-flash-thinking-exp":
                            x = re.findall(r"boxed\{" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)" + r"\}", entry)
                            if len(x) == 0:
                                x = re.findall("[Ff]inal" + ' ' + "*" + "[Aa]nswer:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                                if len(x) == 0:
                                    x = re.findall("[Ss]olution:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                                    if len(x) == 0:
                                        x = re.findall("[Aa][Nn][Ss][Ww][Ee][Rr]:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                            try:
                                (answer) = x.pop()
                                new_entry = float(answer)
                            except Exception as e:
                                new_entry = remember.search_answer("q104",entry).replace(" ", "").replace("\n", "").replace(";", "")

            write_entry(Path(os.path.join(out_path,"q104"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q105(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.lower().replace("years","").replace("solution","").replace(":","").replace("!","").replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(",","")
        if new_entry != "":
            if new_entry != "@" and new_entry != "#":
                try:
                    new_entry = float(new_entry)
                    new_entry = int(new_entry)
                except:
                    new_entry = remember.search_answer("q105",entry)
            write_entry(Path(os.path.join(out_path,"q105"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q106(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,distance\n"
    new_entry_int = None
    solution = [1,3,6,9,4,5,8,2,7,5,7,2,1,3,8,6,4,9,8,4,9,2,7,6,5,3,1,3,2,8,7,5,1,4,9,6,4,5,7,6,9,3,2,1,8,9,6,1,4,8,2,7,5,3,7,8,3,5,1,4,9,6,2,2,9,4,3,6,7,1,8,5,6,1,5,8,2,9,3,7,4]
    for entry in entries:
        new_entry = entry.replace(string.ascii_letters,"").replace("\r", "").replace("\t", "").replace("`","").replace("[","").replace("]","").replace("|","").replace("-","").replace(" ", ",").replace("\n", ",").replace(";",",").strip(",")
        if new_entry.replace(",","") != "":
            if new_entry.replace(",","") != "#" and new_entry.replace(",","") != "@":
                new_entry = new_entry.split(",")
                def filter_fx(a:str) -> bool:
                    if a is not None and a.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "") != "":
                        return True
                    return False
                new_entry = list(filter(filter_fx, new_entry))
                try:
                    new_entry_int = [-1] * len(new_entry)
                    for i,n in enumerate(new_entry):
                        new_entry_int[i] = int(n)
                    if len(new_entry_int) != len(solution):
                        new_entry = "+"
                except:
                    new_entry = remember.search_answer("q106",entry)
                    if new_entry != "+":
                        new_entry = new_entry.replace("\r", "").replace("\t", "").replace("`","").replace("[","").replace("]","").replace("|","").replace("-","").replace(" ", ",").replace("\n", ",").replace(";",",").strip(",")
                        new_entry = new_entry.split(",")
                        new_entry = list(filter(filter_fx, new_entry))
                        new_entry_int = [-1] * len(solution)
                        for i, n in enumerate(new_entry):
                            new_entry_int[i] = int(n)
            else:
                new_entry = new_entry.replace(",", "")
            if new_entry == "+" or new_entry == "#" or new_entry == "@":
                distance = new_entry
            else:
                distance = 0
                if new_entry_int is None:
                    raise Exception("new_entry_int is None")
                for i, n in enumerate(new_entry_int):
                    distance += math.pow(n - solution[i], 2)
                distance = math.sqrt(distance)
            write_entry(Path(os.path.join(out_path,"q106"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,distance)


def q201(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q201",entry)
            write_entry(Path(os.path.join(out_path,"q201"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q202(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                print(entry)
                new_entry = remember.search_answer("q202",entry)
            write_entry(Path(os.path.join(out_path,"q202"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q203(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                print(entry)
                new_entry = remember.search_answer("q203",entry)
            write_entry(Path(os.path.join(out_path,"q203"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)


def q204(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                print(entry)
                new_entry = remember.search_answer("q204",entry)
            write_entry(Path(os.path.join(out_path,"q204"+"_"+model+"_"+q_type+".csv")),header,model,account,q_type,new_entry)

def q205(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    print("Question 205")

def q206(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    print("Question 206")

def q301(entries: list[str], out: TextIO):
    print("Question 301")


def q302(entries: list[str], out: TextIO):
    print("Question 302")


def q303(entries: list[str], out: TextIO):
    print("Question 303")


def q304(entries: list[str], out: TextIO):
    print("Question 304")


def q305(entries: list[str], out: TextIO):
    print("Question 305")


def q306(entries: list[str], out: TextIO):
    print("Question 306")


def q307(entries: list[str], out: TextIO):
    print("Question 307")


def q308(entries: list[str], out: TextIO):
    print("Question 308")


def q309(entries: list[str], out: TextIO):
    print("Question 309")


def q310(entries: list[str], out: TextIO):
    print("Question 310")



