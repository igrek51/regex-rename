from nuclear import CliBuilder, argument, flag

from .bulk import bulk_rename
from .version import __version__


def main():
    CliBuilder('regex-rename', version=__version__, run=bulk_rename, help_on_empty=True,
               help='Regular expressions bulk rename tool for multiple files').has(
        argument('pattern', help='Regex pattern to match filenames'),
        argument('replacement', required=False, help='Replacement regex pattern for renamed files. '
                                                     'Use \\1, \\2 syntax to make use of matched groups'),
        flag('rename', 'r', help='Does actual renaming files instead of just testing replacement pattern'),
        flag('full', help='Enforces matching full filename against pattern'),
    ).run()
