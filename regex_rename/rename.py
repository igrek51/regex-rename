import re
from pathlib import Path
import os
import select
import sys
from typing import Dict, Optional, List, Iterable

from nuclear.sublog import logger

from regex_rename.match import Match, log_match_info
from regex_rename.params import RenameParams


def bulk_rename(
    params: RenameParams,
) -> List[Match]:
    """
    Rename (or match) multiple files at once
    :param pattern: regex pattern to match filenames
    :param replacement: replacement regex pattern for renamed files. 
    Use \\1 syntax to make use of matched groups
    :param dry_run: True - just testing replacement pattern, False - do actual renaming files
    :param full: whether to enforce matching full filename against pattern
    :param recursive: whether to search directories recursively
    :param padding: applies padding with zeros with given length on matched numerical groups
    """
    if not params.dry_run and not params.replacement_pattern:
        raise RuntimeError('replacement pattern is required for actual renaming')

    logger.debug('matching regular expression pattern to files:',
              pattern=params.match_pattern, replacement=params.replacement_pattern, dry_run=params.dry_run,
              full_match=params.full, recursive=params.recursive, padding=params.padding)
    input_files: Iterable[Path] = get_input_files(recursive=params.recursive)
    mismatched: List[str] = []
    matches_iterator: Iterable[Match] = match_files(input_files, params.match_pattern, params.replacement_pattern,
                                                    full=params.full, padding=params.padding, mismatched=mismatched)
    matches: List[Match] = process_matches(matches_iterator, dry_run=params.dry_run, collate=params.collate)

    if params.replacement_pattern:
        check_duplicates(matches)

    if mismatched:
        logger.warn('some files did not match the pattern:', count=len(mismatched), mismatched_names=_format_short_list(mismatched))
    if params.dry_run:
        if matches:
            logger.info('files matched the pattern:', matched=len(matches), mismatched=len(mismatched))
        else:
            logger.warn('no files match the pattern:', matched=len(matches), mismatched=len(mismatched))
    elif params.replacement_pattern:
        rename_matches(matches)
        if matches:
            logger.info('files renamed:', renamed=len(matches), mismatched=len(mismatched))
        else:
            logger.warn('no files match the pattern:', matched=len(matches), mismatched=len(mismatched))

    return matches


def get_input_files(
    root: Optional[Path] = None,
    recursive: bool = False,
) -> Iterable[Path]:
    try:
        stdin_fileno: int = sys.stdin.fileno()
        if not os.isatty(stdin_fileno):  # files piped through stdin
            if select.select([sys.stdin, ], [], [], 0.0)[0]:
                logger.debug('reading input files from stdin')
                for line in sys.stdin:
                    yield Path(line.strip())
                return
    except BaseException as e:
        logger.error(f"Can't read from stdin: {e}")
    
    if not root:
        root = Path()

    if recursive:
        yield from sorted(
            (f.relative_to(root) for f in root.rglob("*")),
            key=lambda f: (f.is_dir(), f.as_posix()),  # rename folders in the end
        )
    else:
        yield from sorted(
            (f for f in root.iterdir()),
            key=lambda f: (f.is_dir(), f.as_posix()),
        )


def match_files(
    files: Iterable[Path],
    match_pattern: str,
    replacement_pattern: Optional[str] = None,
    full: bool = False,
    padding: int = 0,
    mismatched: List[str] = [],
) -> Iterable[Match]:
    for file in files:
        filename = str(file)
        match: Optional[Match] = match_filename(filename, match_pattern, replacement_pattern, full, padding) 
        if match is None:
            mismatched.append(filename)
        else:
            yield match


def match_filename(
    filename: str,
    match_pattern: str, 
    replacement_pattern: Optional[str], 
    full: bool = False, 
    padding: int = 0,
) -> Optional[Match]:
    re_match = match_regex_string(match_pattern, filename, full)
    if not re_match:
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


def validate_replacement(re_match: re.Match, replacement_pattern: str):
    """Test if it's valid in terms of regex rules"""
    simplified = replacement_pattern.replace('\\L', '').replace('\\U', '')
    simplified = re.sub(r'\\P(\d+)', '', simplified)
    re_match.expand(simplified)


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


def process_matches(
    matches_iterator: Iterable[Match],
    dry_run: bool,
    collate: bool,
) -> List[Match]:
    matches: List[Match] = []
    for match in matches_iterator:
        log_match_info(match, dry_run, collate)
        matches.append(match)
    return matches


def check_duplicates(matches: List[Match]):
    names: List[str] = [match.name_to for match in matches if match.name_to]
    duplicates = set((name for name in names if names.count(name) > 1))
    if duplicates:
        duplicates_desc = ', '.join(sorted(duplicates))
        raise RuntimeError(f'aborting - found duplicate filenames after replacement: {duplicates_desc}')


def rename_matches(matches: List[Match]):
    for match in matches:
        assert match.name_to
        Path(match.name_to).parent.mkdir(parents=True, exist_ok=True)
        Path(match.name_from).rename(match.name_to)


def _format_short_list(items: List[str]) -> str:
    if len(items) > 20:
        items = items[:20]
        return ', '.join(items) + ', …'
    else:
        return ', '.join(items)
