import os
from pathlib import Path
from typing import Set

import pytest

from regex_rename.rename import bulk_rename
from regex_rename.params import RenameParams


def test_bulk_rename():
    cwd = os.getcwd()
    os.chdir('tests/res')
    cleanup_names = [
        "Stanis_aw+Lem+Niezwyci__ony+(1).mp3",
        "Stanis_aw+Lem+Niezwyci__ony+(02).mp3",
        "Stanis_aw+Lem+Niezwyci__ony+(03).mp3",
        '01 Niezwyciężony.mp3',
        '02 Niezwyciężony.mp3',
        '03 Niezwyciężony.mp3',
    ]
    for name in cleanup_names:
        if Path(name).exists():
            Path(name).unlink()
    try:
        Path("Stanis_aw+Lem+Niezwyci__ony+(1).mp3").touch()
        Path("Stanis_aw+Lem+Niezwyci__ony+(02).mp3").touch()
        Path("Stanis_aw+Lem+Niezwyci__ony+(03).mp3").touch()

        bulk_rename(RenameParams(
            match_pattern=r'.+\((\d{1,2})\).mp3',
            replacement_pattern=r'\1 Niezwyciężony.mp3',
            dry_run=True,
            padding=2,
        ))

        assert _list_files() != {'01 Niezwyciężony.mp3', '02 Niezwyciężony.mp3', '03 Niezwyciężony.mp3', 'some-0ther-file.txt'}

        bulk_rename(RenameParams(
            match_pattern=r'.+\((\d{1,2})\).mp3',
            replacement_pattern=r'\1 Niezwyciężony.mp3',
            dry_run=False,
            padding=2,
        ))

        assert _list_files() == {'01 Niezwyciężony.mp3', '02 Niezwyciężony.mp3', '03 Niezwyciężony.mp3', 'some-0ther-file.txt'}

    finally:
        for name in cleanup_names:
            if Path(name).exists():
                Path(name).unlink()
        os.chdir(cwd)


def test_match_without_replace():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res/2mp3')

        matches = bulk_rename(RenameParams(
            match_pattern=r'(\d+)\.(.+)',
            dry_run=True,
        ))
        assert len(matches) == 2
        match = matches[0]
        assert match.name_from == '_1.mp3'
        assert match.name_to == None
        assert match.groups == {1: '1', 2: 'mp3'}

    finally:
        os.chdir(cwd)


def test_no_replacement_nor_testing():
    with pytest.raises(RuntimeError) as excinfo:
        bulk_rename(RenameParams(
            match_pattern=r'(\d+).*\.(.+)',
            dry_run=False,
        ))
    assert 'replacement pattern is required for actual renaming' in str(excinfo.value)


def _list_files() -> Set[str]:
    return set([str(f) for f in Path().iterdir() if f.is_file()])
