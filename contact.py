from datetime import date
from typing import List
import uuid
from entity import Entity  

class Contact(Entity):
    def __init__(self,
        name: str,
        surname: str,
        phones: List[str],
        email: str,
        birthday: date,
        tags: List[str] = None
    ):
        super().__init__(tags)
        self.contact_id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.phones = phones
        self.email = email
        self.birthday = birthday


    def __str__(self):
        return (
            f"ID: {self.contact_id}\n"
            f"Name: {self.name} {self.surname}\n"
            f"Phones: {', '.join(self.phones)}\n"
            f"Email: {self.email}\n"
            f"Birthday: {self.birthday.strftime('%Y-%m-%d')}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}"
        )
    
    def edit(self, changes: dict):
        for key, value in changes.items():
            if hasattr(self, key):
                setattr(self, key, value)
