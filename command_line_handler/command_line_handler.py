import pickle
import sys
from pathlib import Path

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
        address_book_save = Path(__file__).parent / "address_book.pkl"
        notebook_save = Path(__file__).parent / "notebook.pkl"
        self.__address_book = pickle.load(address_book_save.open("rb")) if address_book_save.exists() else None
        self.__notebook = pickle.load(notebook_save.open("rb")) if notebook_save.exists() else None
        self.__prompt = ConsolePrompt("[bold][green]Assistant[/green]>[/bold]")

    def __get_command(self):
        return str(self.__prompt)

    def __confirm(self, question: str) -> bool:
        InfoPanel("Confirm", question).show()

        answer = str(ConsolePrompt("Make your choice", ["y", "n"]))

        return answer == "y"

    def handle_command(self):
        command = self.__get_command()
        if command in self.command_map:
            getattr(self, self.command_map[command])()
        else:
            ErrorPanel("Command execution failed", f"Command '{command}' not found").show()

    @keyboard_interrupt_handler
    def add_entity(self):
        """Adds Contact or Note to the address book or notebook"""
        SelectionTree("Who should I add?", ["1. Contact", "2. Note", "3. Exit Command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["1", "2", "3"]))

        if question_prompt == "1":
            InfoPanel("Add Contact", "Not yet implemented").show()
        elif question_prompt == "2":
            InfoPanel("Add Note", "Not yet implemented").show()
        else:
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                self.add_entity()

    @keyboard_interrupt_handler
    def delete_entity(self):
        """Deletes Contact or Note from the address book or notebook"""
        SelectionTree("Who should I delete?", ["1. Contact", "2. Note", "3. Exit Command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["1", "2", "3"]))

        if question_prompt == "1":
            InfoPanel("Delete Contact", "Not yet implemented").show()
        elif question_prompt == "2":
            InfoPanel("Delete Note", "Not yet implemented").show()
        else:
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                self.delete_entity()

    @keyboard_interrupt_handler
    def edit_entity(self):
        """Edits Contact or Note in the address book or notebook"""
        SelectionTree("Who should I edit?", ["1. Contact", "2. Note", "3. Exit Command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["1", "2", "3"]))
        if question_prompt == "1":
            InfoPanel("Edit Contact", "Not yet implemented").show()
        elif question_prompt == "2":
            InfoPanel("Edit Note", "Not yet implemented").show()
        else:
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                self.edit_entity()

    @keyboard_interrupt_handler
    def search_entity(self):
        """Searches Contact or Note in the address book or notebook"""
        SelectionTree("Who should I search?", ["1. Contact", "2. Note", "3. Exit Command"]).show()
        question_prompt = str(ConsolePrompt("Please make your selection", ["1", "2", "3"]))
        if question_prompt == "1":
            InfoPanel("Search Contact", "Not yet implemented").show()
        elif question_prompt == "2":
            InfoPanel("Search Note", "Not yet implemented").show()
        else:
            choice = self.__confirm("Do you want to exit?")
            if choice:
                return
            else:
                self.search_entity()

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

    #def __del__(self):
    #    pass


