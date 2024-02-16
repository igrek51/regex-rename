from typing import Optional

from nuclear import CliBuilder, argument, flag, parameter
from regex_rename.logging import set_short_logs_format

from regex_rename.params import RenameParams
from regex_rename.rename import bulk_rename
from regex_rename.version import __version__


def main():
    CliBuilder(
        'regex-rename', version=__version__, run=_bulk_rename, help_on_empty=True, log_error=True,
        help='Bulk rename tool based on regular expressions to rename multiple files at once',
    ).has(
        argument('pattern', help='Regex pattern to match filenames'),
        argument('replacement', required=False,
                 help='Replacement regex pattern for renamed files. '
                      'Use \\1, \\2 syntax to fill in the matched groups'),
        flag('rename', 'r', help='Does actual file renaming instead of dry-run (testing) mode'),
        flag('full', help='Enforce matching full filename against pattern'),
        flag('recursive', help='Search directories recursively'),
        flag('collate', help='Compare source filenames with the replaced names'),
        flag('short', help='Print output in short, less verbose format without time'),
        parameter('pad-to', type=int, 
                  help='Applies padding with leading zeros with given length on matched numerical groups'),
    ).run()


def _bulk_rename(
    pattern: str,
    replacement: Optional[str],
    rename: bool = False,
    full: bool = False,
    recursive: bool = False,
    collate: bool = False,
    short: bool = False,
    pad_to: int = 0,
):
    if short:
        set_short_logs_format()
    params = RenameParams(
        match_pattern=pattern,
        replacement_pattern=replacement,
        dry_run=not rename,
        full=full,
        recursive=recursive,
        collate=collate,
        padding=pad_to,
    )
    bulk_rename(params)
