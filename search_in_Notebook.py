def search(self, query: str) -> List[Note]:
    
    results = []
    query_lower = query.lower()
    for note in self.notes:
        if (
            query_lower in note.title.lower() or
            query_lower in note.content.lower() or
            any(query_lower in tag.lower() for tag in note.tags)
        ):
            results.append(note)
    return results