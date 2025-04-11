# This module defines the NoteBookEdit class, which is used to represent the changes to be made to a notebook.

from dataclasses import dataclass # Importing dataclass for creating data classes
from typing import List # Importing List for type hinting

@dataclass # This class is used to represent the changes to be made to a notebook.
class NoteBookEdit:   # This class is used to represent the changes to be made to a notebook.
    name: str = None # Default None for name
    description: str = None # Default None for description
    tags: List[str] = None # Default None for tags
