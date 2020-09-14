import os

from nuclear.utils.shell import shell

from regex_rename.bulk import bulk_rename

from pathlib import Path


def test_bulk_rename():
    cwd = os.getcwd()
    try:
        os.chdir('tests/res')

        shell(f'touch "Stanis▯aw+Lem+Niezwyci▯▯ony+(1).mp3"')
        shell(f'touch "Stanis▯aw+Lem+Niezwyci▯▯ony+(02).mp3"')
        shell(f'touch "Stanis▯aw+Lem+Niezwyci▯▯ony+(03).mp3"')

        bulk_rename(r'.+\((\d{1,2})\).+', r'\1 Niezwyciężony.mp3', rename=False, full=False, pad_to=2)
        bulk_rename(r'.+\((\d{1,2})\).+', r'\1 Niezwyciężony.mp3', rename=True, full=False, pad_to=2)

        files = set([str(f) for f in Path().iterdir()])
        assert files == {'01 Niezwyciężony.mp3', '02 Niezwyciężony.mp3', '03 Niezwyciężony.mp3', 'some-other-file.txt'}

        for idx in range(3):
            shell(f'rm "0{idx+1} Niezwyciężony.mp3"')

    finally:
        os.chdir(cwd)
