class NoteSearch:
    def __init__(self, subject_part: str = "", text_part: str = ""):
        self.subject_part = subject_part
        self.text_part = text_part

    def __repr__(self):
        return f"NoteSearch(subject_part={self.subject_part!r}, text_part={self.text_part!r})"
