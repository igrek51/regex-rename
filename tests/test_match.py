from regex_rename.rename import match_filename


def test_full_match():
    match = match_filename('_07.mp3', r'_(\d+).mp3', '\\1_NeverGonnaGiveYouUp.mp3',
                           full=True)
    assert match is not None, 'full match should cover everything'
    assert match.name_to == '07_NeverGonnaGiveYouUp.mp3'

    match = match_filename('_07.mp3', r'(\d+)', '\\1_NeverGonnaGiveYouUp.mp3',
                           full=True)
    assert match is None

    match = match_filename('_07.mp3', r'_(\d+).mp3', '\\1_NeverGonnaGiveYouUp.mp3',
                           full=False)
    assert match is not None
    assert match.name_to == '07_NeverGonnaGiveYouUp.mp3'

    match = match_filename('_07.mp3', r'(\d+)', '\\1_NeverGonnaGiveYouUp.mp3',
                           full=False)
    assert match is not None, 'non-full match can apply in the middle of string'
    assert match.name_to == '07_NeverGonnaGiveYouUp.mp3'


def test_numerical_padding():
    match = match_filename('42.mp3', r'(\d+).mp3', '\\1_NeverGonnaGiveYouUp.mp3',
                           padding=3)
    assert match is not None
    assert match.name_to == '042_NeverGonnaGiveYouUp.mp3', 'padding adds leading zeros'

    match = match_filename('42.mp3', r'(\d+).mp3', '\\1_NeverGonnaGiveYouUp.mp3',
                           padding=0)
    assert match is not None
    assert match.name_to == '42_NeverGonnaGiveYouUp.mp3'


def test_numerical_padding_by_prefix():
    match = match_filename('42-1', r'(\d+)-(\d*)', '\\P4\\1 - \\P2\\2.mp3')
    assert match is not None
    assert match.name_to == '0042 - 01.mp3', 'padding adds leading zeros'

    match = match_filename('42.m', r'(\d+).m', '\\P2\\1.mp3')
    assert match is not None
    assert match.name_to == '42.mp3'
