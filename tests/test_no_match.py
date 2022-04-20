from regex_rename.rename import bulk_rename


def test_no_match():
    matches = bulk_rename(r'---DUPA---', r'0.mp3', testing=True)
    assert not matches
    matches = bulk_rename(r'---DUPA---', r'0.mp3', testing=False)
    assert not matches
