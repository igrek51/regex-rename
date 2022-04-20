from regex_rename.bulk import match_filename


def test_file_with_none_group():
    match = match_filename('1.XXX.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           full=False, padding=0, testing=False)
    assert match is not None
    assert match.name_to == '1.XXX.txt'


def test_file_with_none_group_padding():
    match = match_filename('1.XXX.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           full=False, padding=2, testing=False)
    assert match is not None
    assert match.name_to == '01.XXX.txt'


def test_file_without_none_group():
    match = match_filename('1.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           full=False, padding=0, testing=False)
    assert match is not None
    assert match.name_to == '1.txt'


def test_file_without_none_group_padding():
    match = match_filename('1.txt', r'(\d+)(\.XXX)?.txt', '\\1\\2.txt',
                           full=False, padding=2, testing=False)
    assert match is not None
    assert match.name_to == '01.txt'
