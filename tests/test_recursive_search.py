from pathlib import Path

from regex_rename.rename import get_input_files, match_files


def test_search_directories_recursively():
    input_files = get_input_files(Path('tests/res'), recursive=True)
    matches = list(match_files(input_files, r'(.*)\.(.*)', full=True))
    assert len(matches) == 3
    assert matches[0].name_from == '2mp3/_1.mp3'
    assert matches[1].name_from == '2mp3/_2.mp3'
    assert matches[2].name_from == 'some-0ther-file.txt'


def test_match_directories_recursively():
    input_files = get_input_files(Path('tests/res'), recursive=True)
    matches = list(match_files(input_files, r'mp3$', full=False))
    matched_names = [m.name_from for m in matches]
    assert matched_names == [
        '2mp3',
        '2mp3/_1.mp3',
        '2mp3/_2.mp3',
    ]
