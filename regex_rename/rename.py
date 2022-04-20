from ast import Str
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
    recursive: bool = False,
    padding: int = 0,
) -> List[Match]:
    """
    Rename (or match) multiple files at once
    :param pattern: regex pattern to match filenames
    :param replacement: replacement regex pattern for renamed files. 
    Use \\1 syntax to make use of matched groups
    :param testing: True - just testing replacement pattern, False - do actual renaming files
    :param full: whether to enforce matching full filename against pattern
    :param recursive: whether to search directories recursively
    :param padding: applies padding with zeros with given length on matched numerical groups
    """
    log.debug('matching regex pattern',
              pattern=pattern, replacement=replacement_pattern, testing_mode=testing,
              full_match=full, recursive=recursive, padding=padding)

    matches: List[Match] = match_files(Path(), pattern, replacement_pattern, 
                                       recursive, full, padding)
    for match in matches:
        match.log_info(testing)

    if replacement_pattern:
        find_duplicates(matches)

    if testing:
        if matches:
            log.info('files matched', count=len(matches))
        else:
            log.info('no files matched', count=len(matches))
    elif replacement_pattern:
        rename_matches(matches)
        if matches:
            log.info('files renamed', count=len(matches))
        else:
            log.info('no files renamed', count=len(matches))
    else:
        raise RuntimeError('replacement pattern is required for renaming')
        
    return matches


def match_files(
    path: Path,
    pattern: str,
    replacement_pattern: Optional[str],
    recursive: bool,
    full: bool,
    padding: int,
) -> List[Match]:
    files = list_files(path, recursive)
    filenames = sorted([str(f) for f in files])
    matches = [match_filename(filename, pattern, replacement_pattern, full, padding) 
               for filename in filenames]
    return [m for m in matches if m is not None]


def list_files(
    path: Path,
    recursive: bool,
) -> List[Path]:
    if recursive:
        return [f.relative_to(path) for f in path.rglob("*") if f.is_file()]
    else:
        return [f for f in path.iterdir() if f.is_file()]


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

    group_dict: Dict[int, Optional[str]] = {
        index + 1: group for index, group in enumerate(re_match.groups())
    }
    apply_numeric_padding(group_dict, padding)

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


def apply_numeric_padding(group_dict: Dict[int, Optional[str]], padding: int):
    if padding:
        for index, group in group_dict.items():
            if type(group) == str and group.isnumeric():
                group_dict[index] = group.zfill(padding)


def expand_numeric_padding_prefix(
    name: str,
    group_dict: Dict[int, Optional[str]],
):
    re_pattern = re.compile(r'\\P(\d+)\\(\d+)')
    while True:
        padding_match = re_pattern.search(name)
        if not padding_match:
            break

        padding = int(padding_match.group(1))
        index = int(padding_match.group(2))
        assert index in group_dict, f'group index {index} not found'
        group = group_dict[index]
        if group is None:
            group = ''
            name = name.replace(f'\\P{padding}\\{index}', group)
        else:
            assert group.isnumeric(), f'can\'t apply padding to non-numeric group: {group}'
            name = name.replace(f'\\P{padding}\\{index}', group.zfill(padding))

    return name


def validate_replacement(re_match: re.Match, replacement_pattern: str):
    """Test if it's valid in terms of regex rules"""
    simplified = replacement_pattern.replace('\\L', '').replace('\\U', '')
    simplified = re.sub(r'\\P(\d+)', '', simplified)
    re_match.expand(simplified)


def expand_replacement(
    replacement_pattern: str,
    group_dict: Dict[int, Optional[str]],
) -> str:
    new_name = replacement_pattern
    new_name = expand_numeric_padding_prefix(new_name, group_dict)

    for index, group in group_dict.items():
        if group is None or type(group) != str:
            group = ''

        if '\\L' in new_name:
            new_name = new_name.replace(f'\\L\\{index}', group.lower())
        if '\\U' in new_name:
            new_name = new_name.replace(f'\\U\\{index}', group.upper())

        new_name = new_name.replace(f'\\{index}', group)

    return new_name


def find_duplicates(matches: List[Match]):
    names = [match.name_to for match in matches]
    duplicates = set((name for name in names if names.count(name) > 1))
    if duplicates:
        raise RuntimeError(f'found duplicate replacement filenames: {list(duplicates)}')


def rename_matches(matches: List[Match]):
    for match in matches:
        assert match.name_to
        Path(match.name_to).parent.mkdir(parents=True, exist_ok=True)
        Path(match.name_from).rename(match.name_to)
