from regex_rename.rename import bulk_rename


def test_no_match():
    matches = bulk_rename(r'---DUPA---', r'0.mp3', dry_run=True)
    assert not matches
    matches = bulk_rename(r'---DUPA---', r'0.mp3', dry_run=False)
    assert not matches
