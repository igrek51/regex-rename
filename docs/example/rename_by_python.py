import os

from regex_rename.rename import bulk_rename


if __name__ == '__main__':
    os.chdir('tests/res/2mp3')

    matches = bulk_rename(r'(\d+)\.(.+)', replacement_pattern=None, dry_run=True)
    assert len(matches) == 2
    match = matches[0]
    assert match.name_from == '_1.mp3'
    assert match.name_to == None
    assert match.groups == {1: '1', 2: 'mp3'}
