import logging
import sys

from colorama import Fore, Style
from nuclear.sublog import init_logs
from nuclear.utils.strings import strip_ansi_colors


def set_short_logs_format():
    init_logs()
    for handler in logging.getLogger().handlers:
        handler.setFormatter(ShortLogFormatter())


class ShortLogFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)
        self.plain_formatter = logging.Formatter(fmt='%(levelname)s %(message)s')

    log_level_templates = {
        'CRITICAL': f'{Style.BRIGHT + Fore.RED}CRIT {Style.RESET_ALL}',
        'ERROR': f'{Style.BRIGHT + Fore.RED}ERROR{Style.RESET_ALL}',
        'WARNING': f'{Fore.YELLOW}WARN {Style.RESET_ALL}',
        'INFO': f'{Fore.BLUE}INFO {Style.RESET_ALL}',
        'DEBUG': f'{Fore.GREEN}DEBUG{Style.RESET_ALL}',
    }

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname in self.log_level_templates:
            record.levelname = self.log_level_templates[record.levelname].format(record.levelname)
        line: str = self.plain_formatter.format(record)
        if not sys.stdout.isatty():
            line = strip_ansi_colors(line)
        return line
