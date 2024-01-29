from dataclasses import dataclass, field
from typing import Literal, Dict, Any


@dataclass
class Resource:
    name: str
    action: Literal["update", "copy", "mkdir", "new"]
    filename: str
    parameters: Dict[str, Any] = field(default_factory=dict)
