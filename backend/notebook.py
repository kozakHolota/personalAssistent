import pickle
from typing import List
from uuid import UUID

from backend.note import Note
from backend.note_edit_model import NoteEdit
from backend.note_search import NoteSearch
from backend.util import NOTEBOOK_PATH


class NoteBook:
    def __init__(self):
        self.notes: List[Note] = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def delete(self, note_id: UUID):
        self.notes = [note for note in self.notes if note.note_id != note_id]

    def edit(self, note_uuid: UUID, changes_model: NoteEdit) -> bool:
        desired_notes_found = [n for n in self.notes if n.note_id == note_uuid]
        if desired_notes_found:
            note = desired_notes_found[0]
            note.edit(changes_model)
            return True
        else:
            return False

    def search(self, note_search: NoteSearch) -> List[Note]:
        subject_query = note_search.subject_part.lower()
        text_query = note_search.text_part.lower()

        results = []
        for note in self.notes:
            subject_match = subject_query in note.subject.lower() if subject_query else True
            text_match = text_query in note.text.lower() if text_query else True
            tags_match = (set(note_search.tags)).issubset(set(note.tags)) if note_search.tags else True
            if subject_match and text_match and tags_match:
                results.append(note)
        return results

    def save(self):
        pickle.dump(self, NOTEBOOK_PATH.open("wb+"))
