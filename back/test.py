from dataclasses import dataclass
from typing import Union, List, Dict, Optional, Any


@dataclass
class Port:
    name: str
    status: bool


@dataclass
class Device:
    status: str
    model: Optional[str]
    ports: List[Optional[Port]]


c = Port('GE0/0', True)
ports = [c]
d = Device('connected', 'some', ports)

print(c)
print(d)
