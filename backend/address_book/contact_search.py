from datetime import date
from typing import Optional

class ContactSearch:
    def __init__(
        self,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        birthday: Optional[date] = None
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.birthday = birthday
