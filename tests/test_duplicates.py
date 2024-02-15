import os

import pytest

from regex_rename.rename import bulk_rename
from regex_rename.params import RenameParams


def test_duplicates_after_replacement():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res/2mp3')

        with pytest.raises(RuntimeError) as excinfo:
            bulk_rename(RenameParams(
                match_pattern=r'(\d+)\.(.+)',
                replacement_pattern=r'0.mp3',
                dry_run=True,
            ))

        assert 'aborting - found duplicate filenames after replacement: 0.mp3' in str(excinfo.value)

    finally:
        os.chdir(cwd)
