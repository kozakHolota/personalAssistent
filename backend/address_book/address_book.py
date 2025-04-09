import pickle
from uuid import UUID
from typing import List
from contact import Contact
from contact_search import ContactSearch
from decorators import errors



# address book class
class AddressBook:
    def __init__(self):
        self.contacts: List[Contact] = []  # Stores all contact instances


    @errors
    def add(self, contact: Contact):
    
        # Create a search filter to check if a contact with the same name, surname, email, phone, and birthdate already exists
        search = ContactSearch(
            name=contact.name, 
            surname=contact.surname, 
            email=contact.email, 
            phone=contact.phones[0],
            birthday=contact.birthday)         

        # If a contact with the same details already exists, return an error message
        if self.search(search):  
            return "[red]Error: A contact with the same name, surname, email, phone, or birthdate already exists.[/red]"

        # Add the contact to the list if no duplicates are found
        self.contacts.append(contact)
        return f"[green]Contact {contact.name} {contact.surname} added.[/green]"


    @errors
    def search(self, search: ContactSearch) -> List[Contact]:       
        # Search contacts using optional filters: name, surname, email, or phone.      
        results = []
        for contact in self.contacts:
            if search.name and search.name.lower() not in contact.name.lower():
                continue
            if search.surname and search.surname.lower() not in contact.surname.lower():
                continue
            if search.email and search.email.lower() not in contact.email.lower():
                continue
            if search.phone and not any(search.phone in phone for phone in contact.phones):
                continue
            if search.birthday and search.birthday != contact.birthday:
                continue

            results.append(contact)

        self._display_contacts(results)
        return results
    

    @errors
    def edit(self, contact_id: UUID, **kwargs):    
    
        # Find the contact by ID. If not found, return an error message
        contact = next((c for c in self.contacts if c.contact_id == contact_id), None)
        if not contact:
            return f"[red]Contact with ID {contact_id} not found.[/red]"

        # Create a search filter with the new details (use existing contact details if not provided in kwargs)
        search = ContactSearch(
            name=kwargs.get('name', contact.name),
            surname=kwargs.get('surname', contact.surname),
            email=kwargs.get('email', contact.email),
            phone=kwargs.get('phone', contact.phones[0])
        )
        
        # Search for other contacts that match the provided details (excluding the current contact)
        if self.search(search) and contact not in self.search(search):
            return f"[red]Error: A contact with the same name, surname, email, or phone already exists.[/red]"
        
        # Update the contact with the provided changes
        contact.edit(kwargs)
        return f"[yellow]Contact {contact_id} updated.[/yellow]"


    @errors
    def delete(self, contact_id: UUID):
    
        # Find the contact by ID. If not found, return an error message
        contact = next((c for c in self.contacts if c.contact_id == contact_id), None)
        if not contact:
            return f"[red]Contact with ID {contact_id} not found.[/red]"

        # Remove the contact from the list
        self.contacts.remove(contact)
        return f"[red]Contact {contact_id} deleted.[/red]"



    @errors    
    def save(self):
        
        # Open the file for writing in binary mode
        with open("contacts.pkl", "wb") as f:
            # Serialize all contacts to the file using pickle
            pickle.dump(self.contacts, f)

        return f"[cyan]Contacts have been saved to contacts.pkl[/cyan]"