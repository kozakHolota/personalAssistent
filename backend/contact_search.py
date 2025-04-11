from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class ContactSearch:
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None