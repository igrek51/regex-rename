import re
from dataclasses import dataclass
from typing import Dict, Optional

from nuclear.sublog import log


@dataclass
class Match:
    name_from: str
    name_to: Optional[str]
    groups: Dict[int, Optional[str]]
    re_match: re.Match

    def log_info(self, testing: bool):
        group_kwargs = {f'group_{idx}': group for idx, group in self.groups.items()}
        if self.name_to is None:
            log.info('matched file', file=self.name_from, **group_kwargs)
        else:
            if testing:
                log.info('matched file', **{'from': self.name_from, 'to': self.name_to}, **group_kwargs)
            else:
                log.info('renaming file', **{'from': self.name_from, 'to': self.name_to})
