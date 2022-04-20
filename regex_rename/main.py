from typing import Optional
from nuclear import CliBuilder, argument, flag, parameter

from regex_rename.rename import bulk_rename
from regex_rename.version import __version__


def main():
    CliBuilder('regex-rename', version=__version__, run=_bulk_rename, 
               help_on_empty=True, log_error=True,
               help='Bulk rename tool based on regular expressions to rename multiple files at once',
    ).has(
        argument('pattern', help='Regex pattern to match filenames'),
        argument('replacement', required=False,
                 help='Replacement regex pattern for renamed files. '
                      'Use \\1, \\2 syntax to make use of matched groups'),
        flag('rename', 'r', help='Does actual renaming files instead of just testing replacement pattern'),
        flag('full', help='Enforces matching full filename against pattern'),
        flag('recursive', help='Search directories recursively'),
        parameter('pad-to', type=int, 
                  help='Applies padding with leading zeros with given length on matched numerical groups'),
    ).run()


def _bulk_rename(
    pattern: str,
    replacement: Optional[str],
    rename: bool = False,
    full: bool = False,
    recursive: bool = False,
    pad_to: int = 0,
):
    bulk_rename(pattern, replacement, testing=not rename, full=full, 
                recursive=recursive, padding=pad_to)
