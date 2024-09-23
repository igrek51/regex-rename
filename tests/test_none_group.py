from regex_rename.rename import match_filename


def test_file_with_none_group():
    match = match_filename('1.XXX.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           padding=0)
    assert match is not None
    assert match.name_to == '1.XXX.txt'


def test_file_with_none_group_padding():
    match = match_filename('1.XXX.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           padding=2)
    assert match is not None
    assert match.name_to == '01.XXX.txt'


def test_file_without_none_group():
    match = match_filename('1.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           padding=0)
    assert match is not None
    assert match.name_to == '1.txt'


def test_file_without_none_group_padding():
    match = match_filename('1.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           padding=2)
    assert match is not None
    assert match.name_to == '01.txt'


def test_prefix_padding_with_none():
    match = match_filename('1.txt', r'(\d+)(XXX)?.txt', '\\1\\P2\\2.txt')
    assert match is not None
    assert match.name_to == '1.txt'
