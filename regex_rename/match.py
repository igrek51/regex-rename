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


def log_match_info(match: Match, dry_run: bool):
    group_kwargs = {f'group_{idx}': group for idx, group in match.groups.items()}
    if match.name_to is None:
        log.info('matched file:', file=match.name_from, **group_kwargs)
    else:
        if dry_run:
            log.info('matched file:', **{'from': match.name_from, 'to': match.name_to}, **group_kwargs)
        else:
            log.info('renaming file:', **{'from': match.name_from, 'to': match.name_to})
