import os

import pytest

from regex_rename.rename import bulk_rename


def test_no_replacement_nor_testing():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res/2mp3')

        with pytest.raises(RuntimeError) as excinfo:
            bulk_rename(r'(\d+)\.(.+)', r'0.mp3', testing=True)

        assert 'found duplicate replacement filenames: [\'0.mp3\']' in str(excinfo.value)

    finally:
        os.chdir(cwd)
