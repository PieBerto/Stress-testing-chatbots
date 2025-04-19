import os
from io import TextIOWrapper
from pathlib import Path
from typing import TextIO

from filelock import FileLock, BaseFileLock


def read_file(file_path: Path) -> str:
    lock = FileLock(str(file_path) + ".lock")
    with lock:
        my_file: TextIO = open(file_path, "r")
        content = my_file.read()
        my_file.close()
    return content

def _create_out_file(out_file:Path, header:str) -> tuple[TextIOWrapper, BaseFileLock]:
    parent_folder = Path(str(out_file).removesuffix(str(os.path.basename(out_file))))
    if not parent_folder.exists():
        parent_folder.mkdir(parents=True, exist_ok=False)
    lock = FileLock(str(out_file) + ".lock")
    lock.acquire()
    if not out_file.is_file():
        my_file = open(out_file, "x")
        my_file.write(header)
    return open(out_file, "a+"),lock

def write_entry(out_path:Path,header:str,model:str,account:str,q_type:str,entry):
    (out,lock) = _create_out_file(out_path, header)
    out.write(model + "," + account + "," + q_type + "," + str(entry) + "\n")
    out.close()
    lock.release()

