from typing import List

def search_notebooks(notebooks: List[NoteBook], query: str) -> List[NoteBook]:
    
    results = []
    query_lower = query.lower()

    for notebook in notebooks:
        if (
            query_lower in notebook.name.lower() or
            query_lower in notebook.description.lower() or
            any(query_lower in tag.lower() for tag in notebook.tags)
        ):
            results.append(notebook)
            continue  

        for note in notebook.notes:
            if (
                query_lower in note.title.lower() or
                query_lower in note.content.lower() or
                any(query_lower in tag.lower() for tag in note.tags)
            ):
                results.append(notebook)
                break  

    return results