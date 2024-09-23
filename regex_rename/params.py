from dataclasses import dataclass
from typing import Optional


@dataclass
class RenameParams:
    match_pattern: str
    replacement_pattern: Optional[str] = None
    dry_run: bool = True
    full: bool = False
    recursive: bool = False
    collate: bool = False
    padding: int = 0
