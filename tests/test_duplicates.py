import os

import pytest

from regex_rename.rename import bulk_rename


def test_no_replacement_nor_testing():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res/2mp3')

        with pytest.raises(RuntimeError) as excinfo:
            bulk_rename(r'(\d+)\.(.+)', r'0.mp3', dry_run=True)

        assert 'found duplicate filenames after replacement: [\'0.mp3\']' in str(excinfo.value)

    finally:
        os.chdir(cwd)
