import pickle
from datetime import date
from pathlib import Path
from typing import List
from uuid import UUID

from backend.contact import Contact
from backend.contact_model import ContactModel
from backend.contact_search import ContactSearch
from backend.util import ADDRESS_BOOK_PATH


# address book class
class AddressBook:
    def __init__(self):
        self.contacts: List[Contact] = []  # Stores all contact instances


    
    def add(self, contact: Contact):
        # Add the contact to the list if no duplicates are found
        self.contacts.append(contact)


    
    def search(self, search: ContactSearch) -> List[Contact]:
        # Search contacts using optional filters: name, surname, email, phone, birthday.
        if ((not search.name)
                and (not search.surname)
                and (not search.email)
                and (not search.phone)
                and (not search.birthday)
                and not search.tags):
            return self.contacts

        results = []

        for contact in self.contacts:
            print(search.tags)
            print(contact.tags)
            if (
                (not search.name or search.name.lower() in contact.name.lower()) and
                (not search.surname or search.surname.lower() in contact.surname.lower())and
                (not search.email or search.email.lower() in contact.email.lower()) and
                (not search.phone or [phone for phone in contact.phones if phone == search.phone]) and
                (not search.birthday or search.birthday == contact.birthday) and
                    ((set(search.tags)).issubset(set(contact.tags)) if search.tags else True)
            ):
                results.append(contact)

        return results

    def get_birthdays(self, days_limit: str) -> List[Contact]:
        """Gets all contacts with birthdays in the next <days_limit> days."""
        now_date = date.today()
        jubilers = []
        for contact in self.contacts:
            if contact.birthday:
                normalizad_birthday = contact.birthday.replace(year=now_date.year)
                days_to_birthday = (normalizad_birthday - now_date).days
                if days_to_birthday <= int(days_limit):
                    jubilers.append(contact)
        return jubilers

   
    def edit(self, contact_id: UUID, contact_changes: ContactModel):
    
        # Find the contact by ID. If not found, return an error message
        contact = [c for c in self.contacts if c.contact_id == contact_id]
        
        # Update the contact with the provided changes
        if contact:
            contact[0].edit(contact_changes)
            return True
        else:
            return False

   
    def delete(self, contact_id: UUID):
        self.contacts = [c for c in self.contacts if c.contact_id != contact_id]
        
    def save(self):
        """Serialize all contacts and save them to <project_root>/contacts.pkl using pathlib.
        Resolve path to the project root (assuming script is run from anywhere)
        Open the file using Path and save with pickle"""

        pickle.dump(self, ADDRESS_BOOK_PATH.open("wb+"))