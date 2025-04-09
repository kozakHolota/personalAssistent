import uuid # Importing uuid for unique ID generation
from typing import List # Importing List for type hinting
from entity import Entity # assuming Entity is in same 'backend' package
from class_Note import Note  # Assuming we already have Note class in same package

class NoteBook(Entity):
    def __init__(self, name: str, description: str = "", tags: List[str] = None): # Initialize the NoteBook class
        super().__init__(tags) # Initialize the parent class
        self.notebook_id = uuid.uuid4() # Generate a unique ID for the notebook
        self.name = name # Set the name of the notebook
        self.description = description # Set the description of the notebook
        self.notes: List[Note] = [] # Initialize an empty list of notes

    def add_note(self, note: Note): # Method to add a note to the notebook
        self.notes.append(note) # Append the note to the list of notes

    def remove_note_by_id(self, note_id): # Method to remove a note by its ID
        self.notes = [note for note in self.notes if note.note_id != note_id] # Filter out the note with the given ID

    def edit(self, changes_model: "NoteBookEdit"): # Method to edit the notebook
        if changes_model.name is not None: # Check if the name is provided in the changes model
            self.name = changes_model.name # Update the name
        if changes_model.description is not None: # Check if the description is provided in the changes model
            self.description = changes_model.description # Update the description
        if changes_model.tags is not None: # Check if the tags are provided in the changes model
            self.tags = changes_model.tags # Update the tags

    def __str__(self): # String representation of the NoteBook class
        return (
            f"Notebook ID: {self.notebook_id}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}\n"
            f"Notes count: {len(self.notes)}"
        )

from dataclasses import dataclass # Importing dataclass for creating data classes

@dataclass # This class is used to represent the changes to be made to a notebook.
class NoteBookEdit:
    name: str = None # Default None for name
    description: str = None # Default None for description
    tags: List[str] = None # Default None for tags
