from datetime import datetime   # Importing datetime for timestamping
import uuid # Importing uuid for unique ID generation

from backend.note_edit_model import NoteEdit
from backend.entity import Entity

# This code defines a Note class that represents a note with a subject, text, and tags.
# It inherits from the Entity class and implements methods to edit the note.
# The Note class has an initializer that sets the subject, text, and tags.

class Note(Entity):
    def __init__(self, subject: str, text: str, tags: list[str] = None): # Initialize the Note class
        super().__init__(tags) # Initialize the parent class
        self.note_id = uuid.uuid4() # Generate a unique ID for the note
        self.subject = subject # Set the subject of the note
        self.text = text   # Set the text of the note
        self.created_at = datetime.now() # Set the creation time of the note

#
    def __str__(self): # String representation of the Note class
        return ( # Format the string representation
            f"ID: {self.note_id}\n" # Unique ID of the note
            f"Subject: {self.subject}\n" # Subject of the note
            f"Text: {self.text}\n" # Text of the note
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"  # Creation time of the note
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}" # Tags of the note
        )

    def edit(self, changes_model: "NoteEdit"): # Method to edit the note
        if changes_model.subject: # Check if the subject is provided in the changes model
            self.subject = changes_model.subject # Update the subject
        if changes_model.text: # Check if the text is provided in the changes model
            self.text = changes_model.text # Update the text
        if changes_model.tags is not None: # Check if the tags are provided in the changes model
            self.tags = changes_model.tags # Update the tags

