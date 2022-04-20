import os
from pathlib import Path

from regex_rename.rename import bulk_rename


def test_bulk_rename():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res')

        Path("Stanis_aw+Lem+Niezwyci__ony+(1).mp3").touch()
        Path("Stanis_aw+Lem+Niezwyci__ony+(02).mp3").touch()
        Path("Stanis_aw+Lem+Niezwyci__ony+(03).mp3").touch()

        bulk_rename(r'.+\((\d{1,2})\).mp3', r'\1 Niezwyciężony.mp3', testing=True, full=False, padding=2)
        bulk_rename(r'.+\((\d{1,2})\).mp3', r'\1 Niezwyciężony.mp3', testing=False, full=False, padding=2)

        files = set([str(f) for f in Path().iterdir()])
        assert files == {'01 Niezwyciężony.mp3', '02 Niezwyciężony.mp3', '03 Niezwyciężony.mp3', 'some-other-file.txt'}

        for idx in range(3):
            Path(f'0{idx+1} Niezwyciężony.mp3').unlink()

    finally:
        os.chdir(cwd)
