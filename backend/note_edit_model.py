# This module defines the NoteEdit class, which is used to represent the changes to be made to a note.

from dataclasses import dataclass # Importing dataclass for creating data classes
from typing import List # Importing List for type hinting

@dataclass # This class is used to represent the changes to be made to a note.
class NoteEdit:     # This class is used to represent the changes to be made to a note.
    subject: str = "" # Default empty string for subject
    text: str = "" # Default empty string for text
    tags: List[str] = None # Default None for tags
