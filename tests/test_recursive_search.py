import os
from pathlib import Path

import pytest

from regex_rename.rename import match_files


def test_search_directories_recursively():
    matches = match_files(Path('tests/res'), '(.*)\.(.*)', None, True, True, padding=0)
    assert len(matches) == 3
    assert matches[0].name_from == '2mp3/_1.mp3'
    assert matches[1].name_from == '2mp3/_2.mp3'
    assert matches[2].name_from == 'some-0ther-file.txt'
