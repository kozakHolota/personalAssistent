import tempfile
from pathlib import Path

TMP_DIR = tempfile.gettempdir()

ADDRESS_BOOK_PATH = Path(TMP_DIR) / "address_book.pkl"
NOTEBOOK_PATH = Path(TMP_DIR) / "notebook.pkl"