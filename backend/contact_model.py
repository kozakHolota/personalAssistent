from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class ContactModel:
    name: str = ""
    surname: str = ""
    phones: List[str] = None
    email: str = ""
    birthday: date = None
    tags: List[str] = None
