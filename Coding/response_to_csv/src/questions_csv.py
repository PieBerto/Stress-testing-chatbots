import os
from pathlib import Path
from typing import TextIO

from src.file_and_lock import read_file, write_entry

questions = {}

def insert_fx(fx, params):
    global questions
    if questions.get("q101") is None:
        questions["q101"] = list()
    questions["q101"].append((fx,params))

def question_select(filename: Path, out_file: Path, model:str, account:str):
    folder_name = filename.stem
    match folder_name:
        case "Question101":
            iterate(filename,out_file,q101, model, account)
            pass
        case "Question102":
            iterate(filename,out_file,q102, model, account)
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
            #iterate(filename,out_file, q106, model, account)
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
        new_entry = entry.replace(" ","").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
                    new_entry = int (new_entry)
            except:
                print(entry)
                new_entry = input(
                    "Question 101 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"):\t").strip(" \n\t\r")
                print("\n---------------------\n")
            write_entry(Path(os.path.join(out_path,"q101.csv")),header,model,account,q_type,new_entry)


def q102(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    i = 0
    for entry in entries:
        i += 1
        new_entry = (entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                     .replace("$","").replace("€","").replace(",",""))
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
            except Exception as e:
                print("ERROR: "+str(e)+"\n")
                print("CONVERT TO A VALID ANSWER:\n"+entry)
                new_entry = input(
                    "Question 102 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+", iteration: "+str(i)+"): ").strip(" \n\t\r")
                print("\n---------------------\n")
            finally:
                write_entry(Path(os.path.join(out_path,"q102.csv")),header,model,account,q_type,new_entry)


def q103(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
            except:
                print(entry)
                new_entry = input(
                    "Question 103 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
                print("\n---------------------\n")
            write_entry(Path(os.path.join(out_path,"q103.csv")),header,model,account,q_type,new_entry)


def q104(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,x,y\n"
    for entry in entries:
        tmp_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if tmp_entry != "":
            if tmp_entry != "@" and tmp_entry != "#":
                coordinate = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("(","").replace(")","")
                c_list = coordinate.split(",")
                try:
                    x = float(c_list[0])
                    y = float(c_list[1])
                except:
                    print(entry)
                    coordinate = input(
                        "Question 104 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
                    c_list = coordinate.strip().split(",")
                    x = float(c_list[0])
                    y = float(c_list[1])
                    print("\n---------------------\n")
            write_entry(Path(os.path.join(out_path,"q104.csv")),header,model,account,q_type,str(x)+","+str(y)+";")


def q105(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                print(entry)
                new_entry = input(
                    "Question 105 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
                print("\n---------------------\n")
            write_entry(Path(os.path.join(out_path,"q105.csv")),header,model,account,q_type,new_entry)


def q106(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(";",",").strip(",")
        write_entry(Path(os.path.join(out_path,"q106.csv")),header,model,account,q_type,new_entry)


def q201(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    header = "model,account,type,answer\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                print(entry)
                new_entry = input(
                    "Question 201 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
            write_entry(Path(os.path.join(out_path,"q201.csv")),header,model,account,q_type,new_entry)


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
                new_entry = input(
                    "Question 202 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
            write_entry(Path(os.path.join(out_path,"q202.csv")),header,model,account,q_type,new_entry)


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
                new_entry = input(
                    "Question 203 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
            write_entry(Path(os.path.join(out_path,"q203.csv")),header,model,account,q_type,new_entry)


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
                new_entry = input(
                    "Question 204 [# -> wrong source code written], replace the previous entry (file: "+q_type+", in account: "+account+", model: "+model+"): ").strip(" \n\t\r")
            write_entry(Path(os.path.join(out_path,"q204.csv")),header,model,account,q_type,new_entry)

def q205(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    print("Question 205")

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



