import uuid
import pickle
from typing import List
from pathlib import Path
from entity import Entity
from note import Note
from notebook_edit_model import NoteBookEdit
from note_search import NoteSearch

class NoteBook(Entity):
    def __init__(self, name: str, description: str = "", tags: List[str] = None):
        super().__init__(tags)
        self.notebook_id = uuid.uuid4()
        self.name = name
        self.description = description
        self.notes: List[Note] = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def remove_note_by_id(self, note_id):
        self.notes = [note for note in self.notes if note.note_id != note_id]

    def edit(self, changes_model: "NoteBookEdit"):
        if changes_model.name is not None:
            self.name = changes_model.name
        if changes_model.description is not None:
            self.description = changes_model.description
        if changes_model.tags is not None:
            self.tags = changes_model.tags

    def search(self, noteSearch: NoteSearch) -> List[Note]:
        subject_query = noteSearch.subject_part.lower()
        text_query = noteSearch.text_part.lower()

        results = []
        for note in self.notes:
            subject_match = subject_query in note.subject.lower()
            text_match = text_query in note.text.lower()
            if subject_match and text_match:
                results.append(note)
        return results

    def save(self):
        path = Path(__file__).parent.parent / "note.pkl"  # вихід на рівень вище
        with path.open("wb") as f:
            pickle.dump(self, f)

    def __str__(self):
        return (
            f"Notebook ID: {self.notebook_id}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}\n"
            f"Notes count: {len(self.notes)}"
        )
