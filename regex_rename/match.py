import re
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Match(object):
    name_from: str
    name_to: Optional[str]
    groups: Dict[str, str]
    re_match: re.Match
