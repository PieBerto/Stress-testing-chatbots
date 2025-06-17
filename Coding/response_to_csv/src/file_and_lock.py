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
        my_file.close()
    return open(out_file, "a+"),lock

def write_entry(out_path:Path,header:str,entry:list[str]):
    (out,lock) = _create_out_file(out_path, header)
    output_string = ""
    for e in entry:
        output_string += str(e) + ","
    output_string = output_string[:-1] + "\n"
    out.write(output_string)
    out.close()
    lock.release()

