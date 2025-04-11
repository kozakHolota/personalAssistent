from dataclasses import dataclass
from datetime import date
from typing import List
import uuid
from backend.contact_model import ContactModel
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
        super().__init__(tags or [])
        self.contact_id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.phones = phones
        self.email = email
        self.birthday = birthday
        self.tags = tags if tags is not None else []


    def __str__(self):
        return (
            f"ID: {self.contact_id}\n"
            f"Name: {self.name} {self.surname}\n"
            f"Phones: {', '.join(self.phones)}\n"
            f"Email: {self.email}\n"
            f"Birthday: {self.birthday.strftime('%Y-%m-%d')}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}"
        )
    
    def edit(self, entity_model: ContactModel):
        if entity_model.name:
            self.name = entity_model.name
        if entity_model.surname:
            self.surname = entity_model.surname
        if entity_model.phones:
            self.phones = entity_model.phones
        if entity_model.email:
            self.email = entity_model.email
        if entity_model.birthday:
            self.birthday = entity_model.birthday
        if entity_model.tags:
            self.tags = entity_model.tags