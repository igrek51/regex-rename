from regex_rename.rename import bulk_rename
from regex_rename.params import RenameParams


def test_no_match():
    matches = bulk_rename(RenameParams(
        match_pattern=r'---DUPA---',
        replacement_pattern=r'0.mp3',
        dry_run=True,
    ))
    assert not matches
    matches = bulk_rename(RenameParams(
        match_pattern=r'---DUPA---',
        replacement_pattern=r'0.mp3',
        dry_run=False,
    ))
    assert not matches
