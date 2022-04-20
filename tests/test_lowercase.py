from regex_rename.rename import match_filename


def test_replace_lowercase():
    match = match_filename('ABC-DEF.mp3', r'([A-Z]+)-([A-Z]+).mp3', '\\L\\1-\\2.mp3')
    assert match is not None
    assert match.name_to == 'abc-DEF.mp3'


def test_replace_uppercase():
    match = match_filename('abc-def.mp3', r'([a-z]+)-([a-z]+).mp3', '\\1-\\U\\2.mp3')
    assert match is not None
    assert match.name_to == 'abc-DEF.mp3'
