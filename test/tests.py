from sitegen import *
from pathlib import Path
import tempfile
import pytest

@pytest.fixture
def filesys_setup():
    def make_tmp_file(parent: Path, name:str): 
        parent.mkdir(parents=True, exist_ok = True)
        with open(parent/name, 'w') as f: 
            pass

    with tempfile.TemporaryDirectory() as tmpdirname:
        path = Path(tmpdirname)

        nbs = ["1978-99-11", "2021-03-04-something-great", "2013-99-01-first-of-never"]
        mds = ["2021-03-04-something-great", "2013-99-01-first-of-never"]

        [make_tmp_file(path/"_jupyter", f"{_}.ipynb") for _ in nbs]
        [make_tmp_file(path/"_posts", f"{_}.md") for _ in mds]
        yield path


@pytest.fixture
def notebooks(filesys_setup): return Notebooks(filesys_setup / "_jupyter")

@pytest.fixture
def posts(filesys_setup): return Posts(filesys_setup / "_posts")

def test_notebook_read(filesys_setup, notebooks):
    """ test notebooks being set up properly """
    assert len(notebooks) == 3

def test_notebook_invalid(filesys_setup, notebooks):
    """ test notebooks finds an invalid name"""
    assert not notebooks.all_valid

def test_notebook_rename(filesys_setup, notebooks):
    """ test notebooks has no invalid file names after renaming """
    assert not notebooks.all_valid
    notebooks.update_names()
    assert notebooks.all_valid

def test_posts_read(filesys_setup, posts):
    assert len(posts) == 2

def test_posts_invalid(filesys_setup, posts):
    assert not posts.all_valid

def test_nbs_contain(filesys_setup, notebooks):
    """ test __contains__ for Notebook """
    assert "2021-03-04-something-great"  in notebooks

def test_nbs_post_overlap(filesys_setup, notebooks, posts):
    """ test whats in noteboook and not in posts """
    diff = notebooks.filenames - posts.filenames
    assert len(diff) == 1
