def errors(func):
    """Декоратор для обработки ошибок ввода."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: Not enough arguments."
        except ValueError as e:
            return f"Error: {e}"
        except KeyError:
            return "Error: Contact not found."
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper
