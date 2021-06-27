from datetime import datetime
from pathlib import Path
from tzlocal import get_localzone

import os
import re

DIR = Path.home() / "idrisr.github.io/"

def get_files(path, extension): return list(path.glob(f"*.{extension}"))


class Folder:
    def __init__(self, path): self.path = path
    def __len__(self): return len(self.files)
    def __iter__(self): return iter(self.files)

    @property
    def files(self): return get_files(self.path, self.extension)
    @property
    def filenames(self): return set([_.stem for _ in self.files])

    @property
    def all_valid(self): 
        """ check all files have valid names """
        return all([is_valid_name(_) for _ in self.files])
    def __str__(self): return f'{self.path}\n{self.notebooks}'
    def __repr__(self): return f"{self._filenames}"
    def __contains__(self, element): return element in self.filenames


class Notebooks(Folder):
    extension = "ipynb"

    @property
    def notebooks(self): return self.files
    def update_names(self): [rename_notebook(_) 
            for _ in self.notebooks 
            if not is_valid_name(_)]


class Posts(Folder):
    extension = "md"


def is_valid_name(path: Path) -> bool:
    date_prefix = slice(0, 10)
    try:
        datetime.strptime(path.name[date_prefix], "%Y-%m-%d")
        return True
    except Exception:
        return False


def rename_notebook(path):
    dest = path.parent / convert_name(path)
    path.rename(dest)


def convert_name(path):
    """ convert the jupyter notebook name into a valid jeklyll file name """
    local_timezone = get_localzone()
    aware_dt = datetime.fromtimestamp(os.path.getctime(path), local_timezone)
    date = aware_dt.strftime("%Y-%m-%d")
    regex = re.compile("^\d+-?(.+)")
    match = regex.search(path.name)
    if match: stem = match.group(1)
    else: stem = ""

    return f"{date}-{stem}"
