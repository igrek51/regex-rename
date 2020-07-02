from nuclear import CliBuilder, argument, flag

from .bulk import bulk_rename
from .version import __version__


def main():
    CliBuilder('regex-rename', version=__version__, help='Regular expressions bulk rename tool for multiple files',
               run=bulk_rename, help_on_empty=True).has(
        argument('pattern', help='Regex pattern to match filenames'),
        argument('replacement', required=False, help='Replacement regex pattern for renamed files'),
        flag('rename', help='does actual renaming files instead of just testing replacement pattern'),
        flag('full', help='enforces matching full filename to pattern'),
    ).run()
