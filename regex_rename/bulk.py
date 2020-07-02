import os
import re
from pathlib import Path
from typing import Optional

from nuclear.sublog import log, log_error


def bulk_rename(pattern: str, replacement: Optional[str], rename: bool, full: bool):
    with log_error():
        testing = not rename
        log.debug('matching regex pattern', testing_mode=testing, pattern=pattern, replacement=replacement, full_match=full)

        filenames = sorted([str(f) for f in Path().iterdir()])
        matched = sum([match_filename(filename, pattern, replacement, full, testing) for filename in filenames])

        if testing:
            log.debug('files matched', count=matched)
        else:
            log.info('files renamed', count=matched)


def match_filename(filename: str, pattern: str, replacement: Optional[str], full: bool, testing: bool) -> bool:
    if full:
        match = re.fullmatch(pattern, filename)
    else:
        match = re.search(pattern, filename)

    if testing:
        return filename_pattern_testing(filename, pattern, replacement, match)
    else:
        return filename_pattern_rename(filename, pattern, replacement, match)


def filename_pattern_testing(filename: str, pattern: str, replacement: Optional[str], match: re.Match) -> bool:
    if not match:
        log.warn('not matched', file=filename)
        return False

    groups = match.groups()
    group_kwargs = {f'group_{idx + 1}': group for idx, group in enumerate(groups)}

    if not replacement:
        log.info('matched', file=filename, **group_kwargs)
        return True

    new_name = re.sub(pattern, replacement, filename)
    log.info('matched', **{'from': filename, 'to': new_name}, **group_kwargs)
    return True


def filename_pattern_rename(filename: str, pattern: str, replacement: Optional[str], match: re.Match) -> bool:
    if not match:
        return False

    new_name = re.sub(pattern, replacement, filename)
    log.info('renaming file', **{'from': filename, 'to': new_name})
    os.rename(filename, new_name)
    return True
