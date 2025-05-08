import os
from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path

from src.questions_csv import question_select, questions


def thread_fx(fx_param_list):
    for (fx, param) in fx_param_list:
        (entries, out_path, model, account, q_type) = param
        fx(entries, out_path, model, account, q_type)


def deep_search(path: Path, out_file: Path, model: str | None = None, account: str | None = None):
    (_path, folders, _files) = next(os.walk(path))
    for folder in folders:
        if folder.startswith("Question"):
            print("\t\t" + folder)
            if account is None or model is None:
                raise ValueError("Error in recursion: account or model are None")
            else:
                question_select(Path(os.path.join(path, folder)), out_file, model, account)
        elif folder.startswith("account "):
            print("\t" + folder)
            deep_search(Path(os.path.join(path, folder)), out_file, model, folder.replace("account ", ""))
        else:
            print(folder)
            deep_search(Path(os.path.join(path, folder)), out_file, folder)


if __name__ == '__main__':
    base_path = Path("src/../../response/")

    print("DISCOVERING ALL THE FILE TO CONVERT TO CSV\n\n\n")
    deep_search(base_path, Path("src/../../csv"))
    print(
        "\n\n\nSTARTING CSV FILES CREATION:\n" + "Now will be printed the answers that can't be automatically converted, type: '+' if unintelligible, or the result.\n---------------------\n")

    with ThreadPoolExecutor() as executor:
        futures: list[Future] = list()
        for question in questions.values():
            futures.append(executor.submit(thread_fx, question))
        for future in futures:
            future.result()

    print("\n\n\nDONE.")
