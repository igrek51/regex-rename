import os
import re
from pathlib import Path
from typing import Optional

from nuclear.sublog import log, log_error


def bulk_rename(pattern: str, replacement: Optional[str], rename: bool, full: bool):
    with log_error():
        testing = not rename
        if testing:
            if replacement:
                log.info('testing replacement pattern', pattern=pattern, replacement=replacement, full_match=full)
            else:
                log.info('testing pattern matching', pattern=pattern, full_match=full)

        filenames = [str(f) for f in Path().iterdir()]
        matched = sum([match_filename(filename, pattern, replacement, full, testing) for filename in filenames])

        if testing:
            log.info('files matched', count=matched)
        else:
            log.info('files renamed', count=matched)


def match_filename(filename: str, pattern: str, replacement: Optional[str], full: bool, testing: bool) -> bool:
    if full:
        match = re.match(pattern, filename)
    else:
        match = re.search(pattern, filename)

    if testing:
        return filename_pattern_testing(filename, pattern, replacement, match)
    else:
        return filename_pattern_rename(filename, pattern, replacement, match)


def filename_pattern_testing(filename: str, pattern: str, replacement: Optional[str], match: re.Match) -> bool:
    if not match:
        log.warn('pattern not matched', filename=filename)
        return False

    groups = match.groups()
    group_kwargs = {f'group_{idx + 1}': group for idx, group in enumerate(groups)}

    if not replacement:
        log.info('pattern matched', filename=filename, **group_kwargs)
        return True

    new_name = re.sub(pattern, replacement, filename)
    log.info('pattern matched', from_name=filename, to_name=new_name, **group_kwargs)
    return True


def filename_pattern_rename(filename: str, pattern: str, replacement: Optional[str], match: re.Match) -> bool:
    if not match:
        return False

    new_name = re.sub(pattern, replacement, filename)
    log.info('renaming file', from_name=filename, to_name=new_name)
    os.rename(filename, new_name)
    return True
