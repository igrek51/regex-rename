import os

from nuclear.utils.shell import shell

from regex_rename.bulk import bulk_rename

from pathlib import Path


def test_bulk_rename():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res')

        for idx in range(3):
            shell(f'touch "Stanis▯aw+Lem+Niezwyci▯▯ony+(000{idx}).mp3"')

        bulk_rename(r'.+\(00(\d{2})\).+', r'\1-Niezwyciężony.mp3', rename=False, full=False, pad_to=0)

        bulk_rename(r'.+\(00(\d{2})\).+', r'\1-Niezwyciężony.mp3', rename=True, full=False, pad_to=0)

        files = set([str(f) for f in Path().iterdir()])
        assert files == {'00-Niezwyciężony.mp3', '01-Niezwyciężony.mp3', '02-Niezwyciężony.mp3', 'some-other-file.txt'}

        for idx in range(3):
            shell(f'rm "0{idx}-Niezwyciężony.mp3"')

    finally:
        os.chdir(cwd)
