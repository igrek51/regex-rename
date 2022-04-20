import os
import re
from pathlib import Path
from typing import Dict, Optional, List

from nuclear.sublog import log

from regex_rename.match import Match


def bulk_rename(
    pattern: str,
    replacement_pattern: Optional[str],
    testing: bool = True,
    full: bool = False,
    padding: int = 0,
):
    """
    Rename (or match) multiple files at once
    :param pattern: regex pattern to match filenames
    :param replacement: replacement regex pattern for renamed files. 
    Use \\1 syntax to make use of matched groups
    :param testing: True - just testing replacement pattern, False - do actual renaming files
    :param full: whether to enforce matching full filename against pattern
    :param padding: applies padding with zeros with given length on matched numerical groups
    """
    log.debug('matching regex pattern',
              pattern=pattern, replacement=replacement_pattern, full_match=full, 
              padding=padding, testing_mode=testing)

    matched: List[Match] = match_files(Path(), pattern, replacement_pattern, full, padding)
    for match in matched:
        match.log_info(testing)

    if testing:
        log.debug('files matched', count=len(matched))
    elif replacement_pattern:
        rename_matches(matched)
        log.info('files renamed', count=len(matched))
    else:
        raise RuntimeError('replacement pattern is required for renaming')


def match_files(
    path: Path,
    pattern: str,
    replacement_pattern: Optional[str],
    full: bool,
    padding: int,
) -> List[Match]:
    filenames = sorted([str(f) for f in path.iterdir()])
    matched = [match_filename(filename, pattern, replacement_pattern, full, padding) 
               for filename in filenames]
    return [m for m in matched if m is not None]


def match_filename(
    filename: str,
    pattern: str, 
    replacement_pattern: Optional[str], 
    full: bool = False, 
    padding: int = 0,
) -> Optional[Match]:
    re_match = match_regex_string(pattern, filename, full)
    if not re_match:
        log.warn('no match', file=filename)
        return None

    group_dict: Dict[int, Optional[str]] = {index + 1: group for index, group in enumerate(re_match.groups())}
    if padding:
        for index, group in group_dict.items():
            if type(group) == str and group.isnumeric():
                group_dict[index] = group.zfill(padding)

    if not replacement_pattern:
        return Match(name_from=filename, name_to=None, groups=group_dict, re_match=re_match)

    validate_replacement(re_match, replacement_pattern)
    new_name = expand_replacement(replacement_pattern, group_dict)
    return Match(name_from=filename, name_to=new_name, groups=group_dict, re_match=re_match)


def match_regex_string(pattern: str, filename: str, full: bool) -> Optional[re.Match]:
    if full:
        return re.fullmatch(pattern, filename)
    else:
        return re.search(pattern, filename)


def rename_matches(matches: List[Match]):
    names = [match.name_to for match in matches]
    duplicates = [name for name in names if names.count(name) > 1]
    if duplicates:
        raise RuntimeError(f'found duplicate replacement filenames: {duplicates}')

    for match in matches:
        assert match.name_to
        os.rename(match.name_from, match.name_to)


def validate_replacement(re_match: re.Match, replacement_pattern: str):
    """Test if it's valid in terms of regex rules"""
    simplified = replacement_pattern.replace('\\L', '').replace('\\U', '')
    re_match.expand(simplified)


def expand_replacement(
    replacement_pattern: str,
    group_dict: Dict[int, Optional[str]],
) -> str:
    new_name = replacement_pattern
    for index, group in group_dict.items():
        if group is None or type(group) != str:
            group = ''
        if '\\L' in new_name:
            new_name = new_name.replace(f'\\L\\{index}', group.lower())
        if '\\U' in new_name:
            new_name = new_name.replace(f'\\U\\{index}', group.upper())
        new_name = new_name.replace(f'\\{index}', group)
    return new_name
