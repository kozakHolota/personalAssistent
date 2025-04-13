from dataclasses import field, dataclass


@dataclass
class NoteSearch:
        subject_part: str = ""
        text_part: str = ""
        tags: list = field(default_factory=list)
