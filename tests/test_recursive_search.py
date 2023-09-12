from pathlib import Path

from regex_rename.rename import match_files


def test_search_directories_recursively():
    matches = match_files(Path('tests/res'), r'(.*)\.(.*)', None, recursive=True, full=True, padding=0)
    assert len(matches) == 3
    assert matches[0].name_from == '2mp3/_1.mp3'
    assert matches[1].name_from == '2mp3/_2.mp3'
    assert matches[2].name_from == 'some-0ther-file.txt'


def test_match_directories_recursively():
    matches = match_files(Path('tests/res'), r'mp3$', None, recursive=True, full=False, padding=0)
    matched_names = [m.name_from for m in matches]
    assert matched_names == [
        '2mp3',
        '2mp3/_1.mp3',
        '2mp3/_2.mp3',
    ]
