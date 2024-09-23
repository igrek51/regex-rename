import os
from pathlib import Path
import sys
from typing import Set

import mock

from regex_rename.main import main


def test_bulk_rename_cli():
    cwd = os.getcwd()
    try:
        with MockIO('regex-rename', r'.+\((\d{1,2})\).mp3', r'\1 Niezwyciężony.mp3', '--rename', '--pad-to=2'):
            os.chdir('tests/res')

            Path("Stanis_aw+Lem+Niezwyci__ony+(1).mp3").touch()
            Path("Stanis_aw+Lem+Niezwyci__ony+(02).mp3").touch()
            Path("Stanis_aw+Lem+Niezwyci__ony+(03).mp3").touch()

            main()

            assert _list_files() == {'01 Niezwyciężony.mp3', '02 Niezwyciężony.mp3', '03 Niezwyciężony.mp3', 'some-0ther-file.txt'}

            for idx in range(3):
                Path(f'0{idx+1} Niezwyciężony.mp3').unlink()

    finally:
        os.chdir(cwd)


class MockIO:
    def __init__(self, *in_args: str):
        self._mock_args = mock.patch.object(sys, 'argv', list(in_args))

    def __enter__(self):
        self._mock_args.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._mock_args.__exit__(exc_type, exc_value, traceback)


def _list_files() -> Set[str]:
    return set([str(f) for f in Path().iterdir() if f.is_file()])
