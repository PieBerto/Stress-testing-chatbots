import math
import os
import re
import string
from pathlib import Path

from src.AlreadyAnswer import AlreadyAnswer
from src.file_and_lock import read_file, write_entry

questions = []
counter = {}
total = {}
remember = AlreadyAnswer(Path(r"C:\GitHub\Stress-testing-chatbots\Coding\csv\support_file\already_answered.json"))


def stat_csv_out(model:str,q_name: Path) -> str:
    q_name = str(q_name)
    return (f"{model},,,,,,,one_shot,,,Per Account,,,,,,,,,,,,,,,,CoT,,,Per Account,,,,,,,,,,,,,,,,PoT,,,Per Account,,,,,,,,,,,,,,\n"
            +f",Type,Account,% Account,% Type,% Question,% Account and Type,,Account,% Correct,,=TRANSPOSE(UNIQUE(I3:I1048576)),,,,,,,,,,,,,,,,Account,% Correct,,=TRANSPOSE(UNIQUE(AB3:AB1048576)),,,,,,,,,,,,,,,,Account,% Correct,,=TRANSPOSE(UNIQUE(AU3:AU1048576)),,,,,,,,,,,,,\n"
            +f',=FILTER(${q_name}.B:B;${q_name}.A:A=A1;"No Value"),=FILTER(${q_name}.C:C;${q_name}.A:A=A1;"No Value"),=FILTER(${q_name}.L:O;${q_name}.A:A=A1;"No Value"),,,,,=FILTER(C:C;B:B=H1;"No Value"),=FILTER(G:G;B:B=H1;"No Value"),,=FILTER(J:J;I:I=L2;"No Value"),=FILTER(J:J;I:I=M2;"No Value"),=FILTER(J:J;I:I=N2;"No Value"),=FILTER(J:J;I:I=O2;"No Value"),=FILTER(J:J;I:I=P2;"No Value"),=FILTER(J:J;I:I=Q2;"No Value"),=FILTER(J:J;I:I=R2;"No Value"),=FILTER(J:J;I:I=S2;"No Value"),=FILTER(J:J;I:I=T2;"No Value"),=FILTER(J:J;I:I=U2;"No Value"),=FILTER(J:J;I:I=V2;"No Value"),=FILTER(J:J;I:I=W2;"No Value"),=FILTER(J:J;I:I=X2;"No Value"),=FILTER(J:J;I:I=Y2;"No Value"),,,=FILTER(C:C;B:B=AA1;"No Value"),=FILTER(G:G;B:B=AA1;"No Value"),,=FILTER(AC:AC;AB:AB=AE2;"No Value"),=FILTER(AC:AC;AB:AB=AF2;"No Value"),=FILTER(AC:AC;AB:AB=AG2;"No Value"),=FILTER(AC:AC;AB:AB=AH2;"No Value"),=FILTER(AC:AC;AB:AB=AI2;"No Value"),=FILTER(AC:AC;AB:AB=AJ2;"No Value"),=FILTER(AC:AC;AB:AB=AK2;"No Value"),=FILTER(AC:AC;AB:AB=AL2;"No Value"),=FILTER(AC:AC;AB:AB=AM2;"No Value"),=FILTER(AC:AC;AB:AB=AN2;"No Value"),=FILTER(AC:AC;AB:AB=AO2;"No Value"),=FILTER(AC:AC;AB:AB=AP2;"No Value"),=FILTER(AC:AC;AB:AB=AQ2;"No Value"),=FILTER(AC:AC;AB:AB=AR2;"No Value"),,,=FILTER(C:C;B:B=AT1;"No Value"),=FILTER(G:G;B:B=AT1;"No Value"),,=FILTER(AV:AV;AU:AU=AX2;"No Value"),=FILTER(AV:AV;AU:AU=AY2;"No Value"),=FILTER(AV:AV;AU:AU=AZ2;"No Value"),=FILTER(AV:AV;AU:AU=BA2;"No Value"),=FILTER(AV:AV;AU:AU=BB2;"No Value"),=FILTER(AV:AV;AU:AU=BC2;"No Value"),=FILTER(AV:AV;AU:AU=BD2;"No Value"),=FILTER(AV:AV;AU:AU=BE2;"No Value"),=FILTER(AV:AV;AU:AU=BF2;"No Value"),=FILTER(AV:AV;AU:AU=BG2;"No Value"),=FILTER(AV:AV;AU:AU=BH2;"No Value"),=FILTER(AV:AV;AU:AU=BI2;"No Value"),=FILTER(AV:AV;AU:AU=BJ2;"No Value"),=FILTER(AV:AV;AU:AU=BK2;"No Value")\n')
def insert_fx(fx, params):
    global questions
    questions.append((fx,params))

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
            iterate(filename,out_file, q103, model, account)
            pass
        case "Question104":
            iterate(filename,out_file, q104, model, account)
            pass
        case "Question105":
            iterate(filename,out_file, q105, model, account)
            pass
        case "Question106":
            iterate(filename,out_file, q106, model, account)
            pass
        case "Question201":
            iterate(filename,out_file, q201, model, account)
            pass
        case "Question202":
            iterate(filename,out_file, q202, model, account)
            pass
        case "Question203":
            iterate(filename,out_file, q203, model, account)
            pass
        case "Question204":
            iterate(filename,out_file, q204, model, account)
            pass
        case "Question205":
            iterate(filename,out_file, q205, model, account)
            pass
        case "Question206":
            iterate(filename,out_file, q206, model, account)
            pass
        case "Question301":
            iterate(filename,out_file, q301, model, account)
            pass
        case "Question302":
            iterate(filename,out_file, q302, model, account)
            pass
        case "Question303":
            iterate(filename,out_file, q303, model, account)
            pass
        case "Question304":
            iterate(filename,out_file, q304, model, account)
            pass
        case "Question305":
            iterate(filename,out_file, q305, model, account)
            pass
        case "Question306":
            iterate(filename,out_file, q306, model, account)
            pass
        case "Question307":
            iterate(filename,out_file, q307, model, account)
            pass
        case "Question308":
            iterate(filename,out_file, q308, model, account)
            pass
        case "Question309":
            iterate(filename,out_file, q309, model, account)
            pass
        case "Question310":
            iterate(filename,out_file, q310, model, account)
            pass
        case _:
            raise ValueError("folder name: " + folder_name + " has not been recognized.")

def result_elaboration(account:str,q_type:str,q_name:str,model:str,new_entry,solution,right=None,out_path:str|Path="") -> list[str]:
    global counter
    out_path = str(out_path)
    correct = 0
    #Initializing counters and totals
    if counter.get(model+q_name+q_type+account) is None:
        counter[model + q_name + q_type + account] = 0
    if total.get(model+q_name+q_type+account) is None:
        total[model + q_name + q_type + account] = 0
    if counter.get(model+q_name+q_type) is None:
        counter[model + q_name + q_type] = 0
    if total.get(model+q_name+q_type) is None:
        total[model + q_name + q_type] = 0
    if counter.get(model+q_name+account) is None:
        counter[model+q_name+account] = 0
    if total.get(model+q_name+account) is None:
        total[model+q_name+account] = 0
    if counter.get(model+q_name) is None:
        counter[model+q_name] = 0
        #New model means new csv page:
        write_entry(Path(os.path.join(out_path,q_name+"_"+model+".csv")),stat_csv_out(model,q_name),[""])
    if total.get(model+q_name) is None:
        total[model+q_name] = 0

    #Total counting
    total[model + q_name + q_type + account] += 1
    total[model + q_name + q_type] += 1
    total[model+q_name+account] += 1
    total[model+q_name] += 1
    #The answer is right?
    is_true = False
    if right is None:
        is_true = new_entry == solution
    else: #Right is not None in Question 106 + Question >300
        is_true = right
    #Counter counting
    if is_true:
        correct = 1
        counter[model + q_name + q_type + account] += 1
        counter[model + q_name + q_type] += 1
        counter[model + q_name + account] += 1
        counter[model + q_name] += 1
    #Writing the entry
    output_entry = [model,q_type, account, str(new_entry), str(correct), str(total[model+q_name+account]), str(total[model+q_name+q_type]),
                str(total[model+q_name]), str(counter[model+q_name+account]), str(counter[model+q_name+q_type]), str(counter[model+q_name]),
                "=" + str(counter[model+q_name+account]) + "/" + str(total[model+q_name+account]),
                "=" + str(counter[model+q_name+q_type]) + "/" + str(total[model+q_name+q_type]),
                "=" + str(counter[model+q_name]) + "/" + str(total[model+q_name]),
                "=" + str(counter[model + q_name + q_type + account]) + "/" + str(total[model + q_name + q_type + account])]
    return output_entry

def iterate(path: Path, out_file:Path, fx, model:str, account:str):
    for path, folders, files in os.walk(path):
        for file_name in files:
            if file_name == "one_shot.txt" or file_name == "CoT.txt" or file_name == "PoT.txt":
                print("\t\t\t"+file_name)
                content: list[str] = read_file(Path(os.path.join(path, file_name))).strip().split("?")
                global questions
                insert_fx(fx,(content,out_file,model,account,file_name.replace(".txt", "")))

def q101(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q101"
    solution = 1
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
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
            output_entry = result_elaboration(account,q_type,q_name,model,new_entry,solution,None,out_path)
            write_entry(Path(os.path.join(out_path,q_name+".csv")),header,output_entry)


def q102(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q102"
    solution: float = 142045.45
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
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
                if new_entry != "@" and new_entry!="#" and new_entry!="+" and math.isclose(float(new_entry), solution, rel_tol=1e-5, abs_tol=10.0):
                    output_entry = result_elaboration(account, q_type, q_name,model, new_entry, None, True,out_path)
                else:
                    output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, False,out_path)
                write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q103(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q103"
    solution = 90704
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("$","").replace("€","").replace(",","")
        if new_entry != "":
            try:
                if new_entry != "@" and new_entry != "#":
                    new_entry = float(new_entry)
            except:
                new_entry = remember.search_answer("q103",entry)
            if new_entry != "@" and new_entry!="#" and new_entry!="+" and math.isclose(float(new_entry), solution, rel_tol=1e-5, abs_tol=10.0):
                output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q104(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q104"
    solution = (2.03,1.82)
    header = "Model,Type,Account,Distance,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    r = re.compile(r"^\d*[.]?\d*$")
    for entry in entries:
        new_entry = entry.lower().replace("final answer:","").replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("(","").replace(")","").replace("pi","3.14")
        if new_entry != "":
            x = None
            y = None
            if new_entry != "@" and new_entry != "#":
                if r.match(new_entry):
                    new_entry = "+"
                else:
                    c_list = new_entry.split(",")
                    try:
                        x = float(c_list[0])
                        y = float(c_list[1])
                        new_entry = str(x) + "," + str(y)
                    except Exception as e:
                        solved = None
                        if model == "gemini-2.0-flash-thinking-exp":
                            match = re.findall(r"boxed\{" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)" + r"\}", entry)
                            if len(match) == 0:
                                match = re.findall("[Ff]inal" + ' ' + "*" + "[Aa]nswer:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                                if len(match) == 0:
                                    match = re.findall("[Ss]olution:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                                    if len(match) == 0:
                                        match = re.findall("[Aa][Nn][Ss][Ww][Ee][Rr]:" + ' ' + "*" + r"\((\d*[.]?\d*\s*,\s*\d*[.]?\d*)\)", entry)
                            try:
                                (answer) = match.pop()
                                x = float(answer.split(",")[0])
                                y = float(answer.split(",")[1])
                                solved = answer
                            except Exception as e:
                                pass
                        if solved is None:
                            new_entry = remember.search_answer("q104",entry).replace(" ", "").replace("\n", "").replace(";", "")
                            if new_entry != "+":
                                x = float(new_entry.split(",")[0])
                                y = float(new_entry.split(",")[1])
                        else:
                            new_entry = solved

            if x and y and new_entry != "@" and new_entry!="#" and new_entry!="+" and math.isclose(x, solution[0], rel_tol=1e-5, abs_tol=0.1) and math.isclose(y, solution[1], rel_tol=1e-5, abs_tol=0.1):
                distance = math.sqrt(pow(solution[0]-x, 2) + pow(solution[1]-y,2))
                output_entry = result_elaboration(account, q_type, q_name, model, distance, None, True,out_path)
            elif x and y and new_entry != "@" and new_entry!="#" and new_entry!="+":
                distance = math.sqrt(pow(solution[0] - x, 2) + pow(solution[1] - y, 2))
                output_entry = result_elaboration(account, q_type, q_name, model, distance, None, False,out_path)
            else:
                new_entry = new_entry.replace(","," ")
                output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, False, out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q105(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q105"
    solution = 92
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.lower().replace("years","").replace("solution","").replace(":","").replace("!","").replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(",","")
        if new_entry != "":
            if new_entry != "@" and new_entry != "#":
                try:
                    new_entry = float(new_entry)
                except:
                    new_entry = remember.search_answer("q105",entry)
            if new_entry != "@" and new_entry != "#" and new_entry != "+" and math.isclose(float(new_entry), solution,
                                                                                           rel_tol=1e-5, abs_tol=1.5):
                output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name, model, new_entry, None, False,out_path)
            write_entry(Path(os.path.join(out_path,q_name+".csv")),header,output_entry)

def q106(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q106"
    header = "Model,Type,Account,Distance,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
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
            output_entry = result_elaboration(account,q_type,q_name,model,distance,None,distance==0,out_path)
            write_entry(Path(os.path.join(out_path,q_name+".csv")),header,output_entry)

def q201(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q201"
    solution = 0
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q201",entry)
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def q202(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q202"
    solution = 0
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = "+"
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def q203(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q203"
    solution = 9
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q203",entry)
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def q204(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q204"
    solution = 8
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q204",entry)
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def q205(entries: list[str], out_path: Path, model:str, account:str, q_type:str):
    q_name = "q205"
    solution = 3
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q205", entry)
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def q206(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q206"
    solution = 3
    header = "Model,Type,Account,Answer,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        if new_entry != "":
            try:
                new_entry = float(new_entry)
                new_entry = int(new_entry)
            except:
                new_entry = remember.search_answer("q206", entry)
            output_entry = result_elaboration(account, q_type, q_name,model, new_entry, solution,None,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def changes_check_301(old_a:list[str],old_b:list[str],new_a:list[str],new_b:list[str]) -> bool:
    if "Z" in old_a:
        old_a = [x for x in old_a if x]
        old_b = [x for x in old_b if x]
        new_a = [x for x in new_a if x]
        new_b = [x for x in new_b if x]
        old_a.sort()
        old_b.sort()
        new_a.sort()
        new_b.sort()
        tmp = old_b
        tmp.extend("Z")
        tmp.sort()
        if new_b == tmp:
            return True
        elif "A" in old_a and "A" not in new_a:
            tmp2 = tmp
            tmp2.extend("A")
            tmp2.sort()
            if tmp2 == new_b:
                return True
        elif "B" in old_a and "B" not in new_a:
            tmp2 = tmp
            tmp2.extend("B")
            tmp2.sort()
            if tmp2 == new_b:
                return True
        elif "C" in old_a and "C" not in new_a:
            tmp2 = tmp
            tmp2.extend("C")
            tmp2.sort()
            if tmp2 == new_b:
                return True
        return False
    elif "Z" in old_b:
        return changes_check_301(old_b,old_a,new_b,new_a)
    else:
        return False

def consistency_check_301(a:list[str],b:list[str]) -> bool:
    a = [x for x in a if x]
    b = [x for x in b if x]
    if len(a) + len(b) == 4:
        if "A" in a and "A" not in b or "A" in b and "A" not in a:
            if "B" in a and "B" not in b or "B" in b and "B" not in a:
                if "C" in a and "C" not in b or "C" in b and "C" not in a:
                    if "Z" in a and "Z" not in b or "Z" in b and "Z" not in a:
                        if "A" in a and "B" in a and "Z" not in a or "A" in b and "B" in b and "Z" not in b:
                            #print("cabbage(A) + goat(B)")
                            return False
                        if "B" in a and "C" in a and "Z" not in a or "B" in b and "C" in b and "Z" not in b:
                            #print("goat(B) + wolf(C)")
                            return False
                        return True
                    else:
                        #print("Z")
                        pass
                else:
                    #print("C")
                    pass
            else:
                #print("B")
                pass
        else:
            #print("A")
            pass
    else:
        #print("sum"+str(len(a) + len(b)))
        pass
    return False

def validity_check(a:list[str])-> bool:
    for el in a:
        if not (el == "A" or el == "B" or el == "C" or el == "Z" or el == ""):
            #print("Wrong element: " + el)
            #print("whole list:\n"+str(a))
            return False
    return True

def q301(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q301"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ","").replace("`","").replace("\\","").replace("\n","").replace("_","").replace("'","")
        if new_entry != "":
            right:bool = True
            #print("---------------------------------------------------------------------------------------------------")
            try:
                passages = new_entry.split(";")
                steps = len(passages)
                for i,passage in enumerate(passages):
                    passage = passage.replace("[","").replace("]","").replace("python","").replace("Cabbage","A").replace("Goat","B").replace("Wolf","C").replace("Farmer","Z")
                    passage = passage.replace("AB","A,B").replace("BA","B,A").replace("AC","A,C").replace("CA","C,A").replace("BC","B,C").replace("CB","C,B").replace("AZ","A,Z").replace("ZA","Z,A").replace("BZ","B,Z").replace("ZB","Z,B").replace("CZ","C,Z").replace("ZC","Z,C").replace("ABC","A,B,C").replace("ACB","A,C,B").replace("CBA","C,B,A").replace("BCA","B,C,A").replace("CAB","C,A,B").replace("BAC","B,A,C").replace("ABCZ","A,B,C,Z").replace("AA","A").replace("BB","B").replace("CC","C").replace("ZZ","Z")
                    tmp_r_l = passage.split("->")
                    left_a: list[str] = tmp_r_l[0].split(",")
                    right_a: list[str] = tmp_r_l[1].split(",")
                    #print(str(left_a) + " -> "+ str(right_a))
                    if not validity_check(left_a) or not validity_check(right_a):
                        raise Exception("invalid answer")
                    right = consistency_check_301(left_a, right_a)
                    if not right:
                        #print("consistency failed")
                        break
                    if i != 0:
                        right = changes_check_301(old[0],old[1],left_a,right_a)
                        if not right:
                            #print("changes failed")
                            break
                    else:
                        tmp_r = [x for x in right_a if x]
                        tmp_l = left_a
                        tmp_r.sort()
                        tmp_l.sort()
                        right_l = ["A","B","C","Z"]
                        right_r = []
                        right_l.sort()
                        right_r.sort()
                        if not (tmp_r == right_r and tmp_l == right_l):
                            #print("Initial configuration is wrong")
                            right = False
                            break
                    old = (left_a, right_a)
                if right:
                    last_passage = passages.pop()
                    tmp_r_l = last_passage.replace("[", "").replace("]", "").split("->")
                    left_a: list[str] = tmp_r_l[0].split(",")
                    right_a: list[str] = tmp_r_l[1].split(",")
                    tmp_r = right_a
                    tmp_l = [x for x in left_a if x]
                    tmp_r.sort()
                    tmp_l.sort()
                    right_l = []
                    right_r = ["A", "B", "C", "Z"]
                    right_l.sort()
                    right_r.sort()
                    if not (tmp_r == right_r and tmp_l == right_l):
                        #print("Final configuration is wrong")
                        right = False
            except:
                #print("Exception thrown")
                right = False
                steps = "+"
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps), None, False,out_path)

            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)



def q302(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q302"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        new_entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
        if new_entry != "":
            right:bool = True
            # print("---------------------------------------------------------------------------------------------------")
            try:
                passages = new_entry.split(";")
                steps = len(passages)
                for i, passage in enumerate(passages):
                    passage = passage.replace("[", "").replace("]", "").replace("python", "").replace("Cabbage",
                                                                                                      "A").replace(
                        "Goat", "B").replace("Wolf", "C").replace("Farmer", "Z")
                    passage = passage.replace("AB", "A,B").replace("BA", "B,A").replace("AC", "A,C").replace("CA",
                                                                                                             "C,A").replace(
                        "BC", "B,C").replace("CB", "C,B").replace("AZ", "A,Z").replace("ZA", "Z,A").replace("BZ",
                                                                                                            "B,Z").replace(
                        "ZB", "Z,B").replace("CZ", "C,Z").replace("ZC", "Z,C").replace("ABC", "A,B,C").replace("ACB",
                                                                                                               "A,C,B").replace(
                        "CBA", "C,B,A").replace("BCA", "B,C,A").replace("CAB", "C,A,B").replace("BAC", "B,A,C").replace(
                        "ABCZ", "A,B,C,Z").replace("AA", "A").replace("BB", "B").replace("CC", "C").replace("ZZ", "Z")
                    tmp_r_l = passage.split("->")
                    left_a: list[str] = tmp_r_l[0].split(",")
                    right_a: list[str] = tmp_r_l[1].split(",")
                    # print(str(left_a) + " -> "+ str(right_a))
                    if not validity_check(left_a) or not validity_check(right_a):
                        raise Exception("invalid answer")
                    right = consistency_check_301(left_a, right_a)
                    if not right:
                        # print("consistency failed")
                        break
                    if i != 0:
                        right = changes_check_301(old[0], old[1], left_a, right_a)
                        if not right:
                            # print("changes failed")
                            break
                    else:
                        tmp_r = [x for x in right_a if x]
                        tmp_l = left_a
                        tmp_r.sort()
                        tmp_l.sort()
                        right_l = ["A", "B", "C", "Z"]
                        right_r = []
                        right_l.sort()
                        right_r.sort()
                        if not (tmp_r == right_r and tmp_l == right_l):
                            # print("Initial configuration is wrong")
                            right = False
                            break
                    old = (left_a, right_a)
                if right:
                    last_passage = passages.pop()
                    tmp_r_l = last_passage.replace("[", "").replace("]", "").split("->")
                    left_a: list[str] = tmp_r_l[0].split(",")
                    right_a: list[str] = tmp_r_l[1].split(",")
                    tmp_r = right_a
                    tmp_l = [x for x in left_a if x]
                    tmp_r.sort()
                    tmp_l.sort()
                    right_l = []
                    right_r = ["A", "B", "C", "Z"]
                    right_l.sort()
                    right_r.sort()
                    if not (tmp_r == right_r and tmp_l == right_l):
                        # print("Final configuration is wrong")
                        right = False
            except:
                # print("Exception thrown")
                right = False
                steps = "+"
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)

def hanoi_tower_step_check(configuration:str, old_configuration: str|None = None, initial_configuration: str = "[L,M,S],[],[]", largest_cylinder_letter:str = "L", medium_big_cylinder_letter:str = "M", medium_small_cylinder_letter:str = "S", optional_smallest_cylinder_letter: str | None = None, is_sussman_not_hanoi:bool = False) -> bool:
    #Creating the lists from the input
    tmp_list = configuration.split("]")
    tmp_list = [x for x in tmp_list if x]
    tmp_list = [x.replace("[","") for x in tmp_list]
    stacks_list: list[list[str]] = list()
    wrong = False
    for stack in tmp_list:
        stack = stack.split(",")
        stacks_list.append([x for x in stack if x])

    if len(stacks_list) != 3:
        #print("length "+ str(len(stacks_list))+"\n"+str(stacks_list))
        raise Exception("Wrong split")
    #Chechink the validity of each element
    for stack in stacks_list:
        for element in stack:
            if not (element == largest_cylinder_letter or element == medium_big_cylinder_letter or element == medium_small_cylinder_letter or element == optional_smallest_cylinder_letter):
                #print("WRONG ELEMENT: " + str(element))
                wrong = True
    if wrong:
        raise Exception("Wrong element.") #SIGNIFICA CHE DEVO METTERE '+' COME STEPS.
    #Checking the presence of each cylinder
    if optional_smallest_cylinder_letter:
        presence_list = [False,False,False,False]
    else:
        presence_list = [False,False,False]
    for stack in stacks_list:
        for cylinder in stack:
            if cylinder == largest_cylinder_letter:
                if presence_list[0]:
                    raise Exception("Too many largest cylinders.")
                presence_list[0] = True
            if cylinder == medium_big_cylinder_letter:
                if presence_list[1]:
                    raise Exception("Too many medium big cylinders.")
                presence_list[1] = True
            if cylinder == medium_small_cylinder_letter:
                if presence_list[2]:
                    raise Exception("Too many medium small cylinders.")
                presence_list[2] = True
            if cylinder == optional_smallest_cylinder_letter:
                if presence_list[3]:
                    raise Exception("Too many optional smallest cylinders.")
                presence_list[3] = True
            if not cylinder:
                raise Exception("None cylinder")
    for presence in presence_list:
        if not presence:
            raise Exception("Missing a cylinder.")
    #Checking the current configuration's cylinder order
    if not is_sussman_not_hanoi:
        for stack in stacks_list:
            for i,cylinder in enumerate(stack):
                if i != 0:
                    if stack[i-1] == largest_cylinder_letter and not (cylinder == medium_big_cylinder_letter or cylinder == medium_small_cylinder_letter or cylinder == optional_smallest_cylinder_letter):
                        return False
                    if stack[i-1] == medium_big_cylinder_letter and not (cylinder == medium_small_cylinder_letter or cylinder == optional_smallest_cylinder_letter):
                        return False
                    if stack[i-1] == medium_small_cylinder_letter and not (cylinder == optional_smallest_cylinder_letter):
                        return False
                    if stack[i-1] == optional_smallest_cylinder_letter:
                        return False

    #Checking the initial configuration
    if not old_configuration:
        if configuration != initial_configuration:
            #print("WRONG INITIAL CONFIGURATION:\n"+configuration)
            raise Exception("Wrong initial configuration.")
    else:
        tmp_list = old_configuration.split("]")
        tmp_list = [x for x in tmp_list if x]
        tmp_list = [x.replace("[", "") for x in tmp_list]
        old_stacks_list: list[list[str]] = list()
        for stack in tmp_list:
            stack = stack.split(",")
            old_stacks_list.append([x for x in stack if x])
        #Checking the move
        if len(old_stacks_list) != len(stacks_list):
            raise Exception("Wrong number of stacks.")
        changed = None
        for i,stack in enumerate(stacks_list):
            if len(old_stacks_list[i]) - len(stack) == 1:
                if changed is not None and changed == old_stacks_list[i].copy().pop():
                    changed = None
                elif changed is None:
                    changed = old_stacks_list[i].copy().pop()
                else:
                    #print("Wrong move")
                    #print("old: " + str(old_stacks_list[i]) + "\nnew: " + str(stack))
                    return False
            elif len(old_stacks_list[i]) - len(stack) == -1:
                if changed is not None and changed == stack.copy().pop():
                    changed = None
                elif changed is None:
                    changed = stack.copy().pop()
                else:
                    #print("Wrong move")
                    #print("old: " + str(old_stacks_list[i]) + "\nnew: " + str(stack))
                    return False
            elif len(old_stacks_list[i]) != len(stack):
                return False #Moved too many cylinders
            minor_len = len(old_stacks_list[i])
            if len(old_stacks_list[i]) > len(stack):
                minor_len = len(stack)
            for pos in range(minor_len):
                if old_stacks_list[i][pos] != stack[pos]:
                    #print("Moved an element from the middle of the list.")
                    return False
        if changed is not None:
            #print("An element has been removed or added incorrectly")
            return False #An element has been removed or added incorrectly
    return True

def q303(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q303"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_","").replace("'","")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config,"[B],[A,C],[]","A","B","C",None,True)
                        if right:
                            right = tmp
                    except Exception as e:
                        #print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    #check final configuration
            if right and old_config:
                if old_config.find("C,B,A")==-1:
                    #print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [B],[A,C],[];[B],[A],[C];[],[A],[C,B];[],[],[C,B,A]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            #print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)



def q304(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q304"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[B],[A,C],[]", "A", "B", "C", None, True)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("C,B,A") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [B],[A,C],[];[B],[A],[C];[],[A],[C,B];[],[],[C,B,A]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q305(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q305"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[L,M,S],[],[]", "L", "M", "S", None, False)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[L,M,S]") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [L,M,S],[],[];[L,M],[],[S];[L],[M],[S];[L],[M,S],[];[],[M,S],[L];[S],[M],[L];[S],[],[L,M];[],[],[L,M,S]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q306(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q306"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[L,M,S],[],[]", "L", "M", "S", None, False)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[L,M,S]") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [L,M,S],[],[];[L,M],[],[S];[L],[M],[S];[L],[M,S],[];[],[M,S],[L];[S],[M],[L];[S],[],[L,M];[],[],[L,M,S]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q307(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q307"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[L,M,S],[],[]", "L", "M", "S", None, False)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[L,M,S]") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [L,M,S],[],[];[L,M],[],[S];[L],[M],[S];[L],[M,S],[];[],[M,S],[L];[S],[M],[L];[S],[],[L,M];[],[],[L,M,S]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q308(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q308"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[A,B,C],[],[]", "A", "B", "C", None, False)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[A,B,C]") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [A,B,C],[],[];[A,B],[],[C];[A],[B],[C];[A],[B,C],[];[],[B,C],[A];[C],[B],[A];[C],[],[A,B];[],[],[A,B,C]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q309(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q309"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "")
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[B,A,D,C],[],[]", "A", "B", "C", "D", True)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[A,B,C,D]") == -1:  # '[L,M,S],[],[];[L,M],[],[S];[L],[M],[S];[L],[M,S],[];[],[M,S],[L];[S],[M],[L];[S],[],[L,M];[],[],[L,M,S]'
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                # example of right: [B,A,D,C],[],[];[B,A,D],[C],[];[B,A],[C,D],[];[B],[C,D],[A];[],[C,D],[A,B];[D],[C],[A,B];[D],[],[A,B,C];[],[],[A,B,C,D]
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)


def q310(entries: list[str], out_path: Path, model: str, account: str, q_type: str):
    q_name = "q310"
    header = "Model,Type,Account,Steps,Correct,Repetition per Account(Model),Repetition per Type(Model),Repetition per Question(Model),Account(Model) Cumulative,Type(Model) Cumulative,Question(Model) Cumulative,Account(Model) Percentual,Type(Model) Percentual,Question(Model) Percentual,Type and Account Percentual\n"
    for entry in entries:
        if entry:
            entry = entry.replace(" ", "").replace("`", "").replace("\\", "").replace("\n", "").replace("_",
                                                                                                        "").replace("'",
                                                                                                                    "").upper()
            steps = entry.split(";")
            steps_count = len(steps)
            right:bool = True
            old_config = None
            for config in steps:
                if config:
                    try:
                        tmp = hanoi_tower_step_check(config, old_config, "[D1,D2,D3,D4],[],[]", "D1", "D2", "D3", "D4", False)
                        if right:
                            right = tmp
                    except Exception as e:
                        # print(str(e)+"\n")
                        right = False
                        steps_count = "+"
                        break
                    old_config = config
                    # check final configuration
            if right and old_config:
                if old_config.find("[],[],[D1,D2,D3,D4]") == -1:
                    # print(str(steps) + "\nDoesn't match the final configuration required\n"+old_config)
                    right = False
            if right:
                #example of right: '[d1,d2,d3,d4],[],[];[d1,d2,d3],[d4],[];[d1,d2],[d4],[d3];[d1,d2],[],[d3,d4];[d1],[d2],[d3,d4];[d1,d4],[d2],[d3];[d1,d4],[d2,d3],[];[d1],[d2,d3,d4],[];[],[d2,d3,d4],[d1];[],[d2,d3],[d1,d4];[d3],[d2],[d1,d4];[d3,d4],[d2],[d1];[d3,d4],[],[d1,d2];[d3],[d4],[d1,d2];[],[d4],[d1,d2,d3];[],[],[d1,d2,d3,d4]'
                #print(str(entry)+"\n\n-----------------------------------------------------------------------------\n")
                pass
            # print(entry+"\n\n------------------------------------------------\n")
            if right:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,True,out_path)
            else:
                output_entry = result_elaboration(account, q_type, q_name,model, str(steps_count), None,False,out_path)
            write_entry(Path(os.path.join(out_path, q_name + ".csv")), header, output_entry)



