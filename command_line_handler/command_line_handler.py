import pickle
import sys
from pathlib import Path
from typing import Callable

from backend.note import Note
from backend.notebook import NoteBook
from command_line_handler.decorators import keyboard_interrupt_handler
from ui_components.panels import ErrorPanel, InfoPanel
from ui_components.prompt import ConsolePrompt
from ui_components.selection_tree import SelectionTree
from ui_components.table import ConsoleTable


class CommandLineHandler:
    command_map = {
        "add": "add_entity",
        "delete": "delete_entity",
        "edit": "edit_entity",
        "search": "search_entity",
        "exit": "exit",
        "help": "help"
    }

    def __init__(self):
        address_book_save = Path("address_book.pkl")
        notebook_save = Path("notebook.pkl")
        self.__address_book = pickle.load(address_book_save.open("rb")) if address_book_save.exists() else None
        self.__notebook = pickle.load(notebook_save.open("rb")) if notebook_save.exists() else NoteBook()
        self.__prompt = ConsolePrompt("[bold][green]Assistant[/green]>[/bold]")

    def __get_command(self):
        """Gets command entered by the user"""
        return str(self.__prompt)

    def __confirm(self, question: str) -> bool:
        """Displays a confirmation prompt and returns the user's choice'"""
        InfoPanel("Confirm", question).show()

        answer = str(ConsolePrompt("Make your choice", ["y", "n"]))

        return answer == "y"

    def handle_command(self):
        """Handles command entered by the user"""
        command = self.__get_command()
        if command in self.command_map:
            getattr(self, self.command_map[command])()
        else:
            ErrorPanel("Command execution failed", f"Command '{command}' not found").show()

    def __choose_entity(self,
                        greating_message: str,
                        caller: Callable,
                        contact_callback: Callable,
                        note_callback: Callable) -> None:
        """Shows selection tree with Contacts and Notes"""
        SelectionTree(greating_message, ["1. Contact", "2. Note", "3. Exit Command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["1", "2", "3"]))

        if question_prompt == "1":
            contact_callback()
        elif question_prompt == "2":
            note_callback()
        else:
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                caller()

    def __add_note(self):
        """Adds Note to the notebook"""
        note_subject = str(ConsolePrompt("Enter the subject of the note"))
        note_text = str(ConsolePrompt("Enter the text of the note"))
        tags = str(ConsolePrompt("Enter the tags of the note, separated by commas"))

        SelectionTree(
            "Do you want to save the note?",
            ["(y) yes", "(n) no, just edit", "(e) exit command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["y", "n", "e"]))

        if question_prompt == "n":
            note_subject = str(ConsolePrompt("Edit subject of the note", default=note_subject))
            note_text = str(ConsolePrompt("Edit text of the note", default=note_text))
            tags = str(ConsolePrompt("Edit tags of the note", default=tags))
        elif question_prompt == "e":
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                self.__add_note()

        try:
            self.__notebook.add_note(Note(note_subject, note_text, tags.split(",")))
            InfoPanel("Note added", f"Note '{note_subject}' added successfully").show()
        except ValueError as e:
            ErrorPanel("Note addition failed", str(e)).show()

    def __search_note(self):
        """Search for notes in the notebook"""
        notes_table = ConsoleTable("Notes", ["Subject", "Text", "Tags"])
        for note in self.__notebook.notes:
            notes_table.add_row([note.subject, note.text, ", ".join(note.tags)])

        notes_table.show()


    @keyboard_interrupt_handler
    def add_entity(self):
        """Adds Contact or Note to the address book or notebook"""
        self.__choose_entity(
            "Who should I add?",
            self.add_entity,
            lambda: InfoPanel("Add Contact", "Not yet implemented").show(),
            self.__add_note
        )

    @keyboard_interrupt_handler
    def delete_entity(self):
        """Deletes Contact or Note from the address book or notebook"""
        self.__choose_entity(
            "Who should I delete?",
            self.delete_entity,
            lambda: InfoPanel("Delete Contact", "Not yet implemented").show(),
            lambda: InfoPanel("Delete Note", "Not yet implemented").show()
        )

    @keyboard_interrupt_handler
    def edit_entity(self):
        """Edits Contact or Note in the address book or notebook"""
        self.__choose_entity(
            "Who should I edit?",
            self.edit_entity,
            lambda: InfoPanel("Edit Contact", "Not yet implemented").show(),
            lambda: InfoPanel("Edit Note", "Not yet implemented").show()
        )

    @keyboard_interrupt_handler
    def search_entity(self):
        """Searches Contact or Note in the address book or notebook"""
        self.__choose_entity(
            "Who should I search?",
            self.search_entity,
            lambda: InfoPanel("Search Contact", "Not yet implemented").show(),
            self.__search_note
        )

    @keyboard_interrupt_handler
    def exit(self):
        """Exits the Adviser"""
        choice = self.__confirm("Do you want to exit?")
        if choice:
            sys.exit(0)
        else:
            return

    @keyboard_interrupt_handler
    def help(self):
        """Lists all commands available in the Adviser"""
        help_table = ConsoleTable("All Commands", ["Command", "Description"])
        for command in self.command_map:
            help_table.add_row([command, getattr(self, self.command_map[command]).__doc__])

        help_table.show()

    def __del__(self):
        """Saves the address book and notebook to disk"""
        self.__notebook.save()


