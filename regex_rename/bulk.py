import os
import re
from pathlib import Path
from typing import Optional, List

from nuclear.sublog import log, log_error

from regex_rename.match import Match


def bulk_rename(pattern: str, replacement: Optional[str], rename: bool, full: bool, pad_to: int):
    with log_error():
        testing = not rename
        log.debug('matching regex pattern',
                  testing_mode=testing, pattern=pattern, replacement=replacement, full_match=full, padding=pad_to)

        filenames = sorted([str(f) for f in Path().iterdir()])
        matched = [match_filename(filename, pattern, replacement, full, pad_to, testing) for filename in filenames]
        matched = list(filter(lambda e: e, matched))

        if testing:
            log.debug('files matched', count=len(matched))
        elif replacement:
            rename_matched(matched)
            log.info('files renamed', count=len(matched))


def match_filename(
    filename: str, 
    pattern: str, 
    replacement: Optional[str], 
    full: bool, 
    padding: int,
    testing: bool,
) -> Optional[Match]:
    if full:
        match = re.fullmatch(pattern, filename)
    else:
        match = re.search(pattern, filename)

    if not match:
        log.warn('no match', file=filename)
        return None

    group_dict = {idx + 1: group for idx, group in enumerate(match.groups())}
    if padding:
        for idx, group in group_dict.items():
            if group.isnumeric():
                group_dict[idx] = group.zfill(padding)

    group_kwargs = {f'group_{idx}': group for idx, group in group_dict.items()}

    if not replacement:
        log.info('matched ', file=filename, **group_kwargs)
        return Match(name_from=filename, name_to=None, groups=group_dict, re_match=match)

    validate_replacement(match, replacement)
    new_name = replacement
    for idx, group in group_dict.items():
        if '\\L' in new_name:
            new_name = new_name.replace(f'\\L\\{idx}', group.lower())
        if '\\U' in new_name:
            new_name = new_name.replace(f'\\U\\{idx}', group.upper())
        new_name = new_name.replace(f'\\{idx}', group)

    if testing:
        log.info('matched ', **{'from': filename, 'to': new_name}, **group_kwargs)
    return Match(name_from=filename, name_to=new_name, groups=group_dict, re_match=match)


def rename_matched(matches: List[Match]):
    names = [match.name_to for match in matches]
    duplicates = [name for name in names if names.count(name) > 1]
    if duplicates:
        raise RuntimeError(f'found duplicates: {duplicates}')
    for match in matches:
        log.info('renaming file', **{'from': match.name_from, 'to': match.name_to})
        os.rename(match.name_from, match.name_to)


def validate_replacement(match: Match, replacement: str):
    """Test if it's valid in terms of regex rules"""
    simplified = replacement.replace('\\L', '').replace('\\U', '')
    match.expand(simplified)
