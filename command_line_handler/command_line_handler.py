import datetime
import pickle
import re
import sys
from typing import Callable

from backend.address_book import AddressBook
from backend.contact import Contact
from backend.contact_model import ContactModel
from backend.contact_search import ContactSearch
from backend.note import Note
from backend.note_edit_model import NoteEdit
from backend.note_search import NoteSearch
from backend.notebook import NoteBook
from backend.util import NOTEBOOK_PATH, ADDRESS_BOOK_PATH
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
        "show birthdays": "show_birthdays",
        "exit": "exit",
        "clear saved data": "clear_saved_data",
        "help": "help"
    }

    def __init__(self):
        self.save_entities: bool = True
        self.__address_book = pickle.load(ADDRESS_BOOK_PATH.open("rb")) if ADDRESS_BOOK_PATH.exists() else AddressBook()
        self.__notebook = pickle.load(NOTEBOOK_PATH.open("rb")) if NOTEBOOK_PATH.exists() else NoteBook()
        self.__prompt = ConsolePrompt("[bold][green]Assistant[/green]>[/bold]")

    def __get_command(self):
        """Gets command entered by the user"""
        try:
            return str(self.__prompt)
        except KeyboardInterrupt:
            print("\n")
            InfoPanel("Confirm", "Do you want to exit?").show()
            answer = str(ConsolePrompt("Make your choice", ["y", "n"]))
            if answer == "y":
                sys.exit(0)
            else:
                return


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
        elif not command:
            print("\n")
        else:
            ErrorPanel("Command execution failed", f"Command '{command}' not found").show()

    def __add_email(self):
        email = str(ConsolePrompt("Enter the email (press enter to skip)"))
        if not email:
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            ErrorPanel("Invalid email", f"Email must be in the format <EMAIL>").show()
            return self.__add_email()
        return email

    def __add_birthday(self):
        birthday = str(
            ConsolePrompt("Enter the birthday of the contact in format: year/month/day (press enter to skip)"))
        if not birthday:
            return
        try:
            return datetime.datetime.strptime(birthday, "%Y/%m/%d")
        except ValueError:
            ErrorPanel("Invalid birthday", f"Birthday must be in the format year/month/day").show()
            return self.__add_birthday()

    def __add_phone(self, phones: list):
        phone_number = str(ConsolePrompt("Enter the phone number (press enter to skip)"))
        if not phone_number:
            return
        if not re.match(r"^\+?\d{10,12}$", phone_number):
            ErrorPanel("Invalid phone number", f"Phone number must be in the format +380123456789").show()
            self.__add_phone(phones)

        phones.append(phone_number)


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
            self.__notebook.add_note(Note(note_subject, note_text, re.split(r"\s*,\s*", tags)))
            InfoPanel("Note added", f"Note '{note_subject}' added successfully").show()
        except ValueError as e:
            ErrorPanel("Note addition failed", str(e)).show()

    def __add_contact(self):
        """Adds Contact to the address book"""
        phones = []

        name = str(ConsolePrompt("Enter the name of the contact"))
        surname = str(ConsolePrompt("Enter the surname of the contact"))
        while True:
            self.__add_phone(phones)
            choice = self.__confirm("Do you want to add another phone number?")
            if not choice:
                break

        email = self.__add_email()
        birthday = self.__add_birthday()
        tags = []
        while True:
            tag = str(ConsolePrompt("Enter the tag of the contact (press enter to skip)"))
            if not tag:
                break
            tags.append(tag)

        try:
            self.__address_book.add(Contact(name, surname, phones, email, birthday, tags))
        except Exception as e:
            ErrorPanel("Contact addition failed", str(e)).show()

    def __search_contact(self):
        """Search for contacts in the address book"""
        name = str(ConsolePrompt("Enter the name of the contact or its part (press enter to skip)"))
        surname = str(ConsolePrompt("Enter the surname of the contact or its part (press enter to skip)"))
        email = self.__add_email()
        birthday = self.__add_birthday()
        phone = str(ConsolePrompt("Enter the phone number of the contact or its part (press enter to skip)"))
        tags = str(ConsolePrompt("Enter the tags of the contact separated by comma (press enter to skip)"))
        found_contacts = self.__address_book.search(ContactSearch(
            name=name,
            surname=surname,
            email=email,
            birthday=birthday,
            phone=phone,
            tags = re.split(r"\s*,\s*", tags) if tags else []))

        if not found_contacts:
            InfoPanel("No contacts found", "No contacts found with the given search criteria").show()
        else:
            contacts_table = ConsoleTable("Contacts", ["No.", "Name", "Surname", "Phones", "Email", "Birthday", "Tags"])
            for contact in found_contacts:
                contacts_table.add_row([
                    str(found_contacts.index(contact) + 1),
                    contact.name,
                    contact.surname,
                    "\n".join(contact.phones),
                    contact.email,
                    contact.birthday.strftime("%Y/%m/%d") ,
                    "\n".join(contact.tags)]
                )
            contacts_table.show()

        return found_contacts

    def __search_note(self):
        """Search for notes in the notebook"""
        subj_part = str(ConsolePrompt("Enter the subject of the note or its part (press enter to skip)"))
        text_part = str(ConsolePrompt("Enter the text of the note or its part (press enter to skip)"))
        tags_part = str(ConsolePrompt("Enter the tags of the note separated by comma (press enter to skip)"))
        found_notes = self.__notebook.search(NoteSearch(subj_part, text_part, re.split(r"\s*,\s*", tags_part) if tags_part else []))
        if not found_notes:
            InfoPanel("No notes found", "No notes found with the given search criteria").show()
        else:
            notes_table = ConsoleTable("Notes", [r"#", "Subject", "Text", "Tags"])
            for note in found_notes:
                notes_table.add_row([
                    str(found_notes.index(note) + 1),
                    note.subject,
                    note.text,
                    ", ".join(note.tags)]
                )

            notes_table.show()

        return found_notes

    def __edit_contact(self):
        """Edits Contact in the address book"""
        found_contacts = self.__search_contact()
        if found_contacts:
            choices = [str(i) for i in range(1, len(found_contacts) + 1)]
            contact_index = int(str(ConsolePrompt("Select the contact to edit", choices))) - 1
            contact = found_contacts[contact_index]
            name = str(ConsolePrompt("Enter the new name of the contact", default=contact.name))
            surname = str(ConsolePrompt("Enter the new surname of the contact", default=contact.surname))
            phones = []
            while True:
                self.__add_phone(phones)
                choice = self.__confirm("Do you want to add another phone number?")
                if not choice:
                    break

            email = self.__add_email()
            birthday = self.__add_birthday()
            tags = []
            while True:
                tag = str(ConsolePrompt("Enter the tag of the contact (press enter to skip)"))
                if not tag:
                    break
                tags.append(tag)

            self.__address_book.edit(
                    contact.contact_id,
                    ContactModel(
                        name=name,
                        surname=surname,
                        phones=phones,
                        email=email,
                        birthday=birthday,
                        tags=tags
                    )
                )
        else:
                ErrorPanel("Contact edit failed", "Contact not found").show()

    def __edit_note(self):
        """Edits selected note in the notebook"""
        found_notes = self.__search_note()

        if found_notes:
            note_index = int(str(ConsolePrompt("Select note to edit", choices=[str(i) for i in range(1, len(found_notes) + 1)]))) - 1
            note = found_notes[note_index]
            subject = str(ConsolePrompt("Enter the new subject of the note", default=note.subject))
            text = str(ConsolePrompt("Enter the new text of the note", default=note.text))
            tags = str(ConsolePrompt("Enter the new tags of the note separated by comma (press enter to skip)", default=", ".join(note.tags)))
            self.__notebook.edit(note.note_id, NoteEdit(subject, text, re.split(r"\s*,\s*", tags)))
        else:
            ErrorPanel("Note edit failed", "Note not found").show()

    def __delete_contact(self):
        """Delete selected contact from the address book"""
        found_contacts = self.__search_contact()

        if found_contacts:
            choices = [str(i) for i in range(1, len(found_contacts) + 1)]
            contact_index = int(str(ConsolePrompt("Select the contact to edit", choices))) - 1
            contact = found_contacts[contact_index]
            self.__address_book.delete(contact.contact_id)
        else:
            ErrorPanel("Contact deletion failed", "Contact not found").show()

    def __delete_note(self):
        """Delete selected note from the notebook"""
        found_notes = self.__search_note()
        if found_notes:
            note_index = int(
                str(ConsolePrompt("Select note to edit", choices=[str(i) for i in range(1, len(found_notes) + 1)]))) - 1
            note = found_notes[note_index]
            self.__notebook.delete(note.note_id)
        else:
            ErrorPanel("Note deletion failed", "Note not found").show()


    @keyboard_interrupt_handler
    def add_entity(self):
        """Adds Contact or Note to the address book or notebook"""
        self.__choose_entity(
            "Who should I add?",
            self.add_entity,
            self.__add_contact,
            self.__add_note
        )

    @keyboard_interrupt_handler
    def delete_entity(self):
        """Deletes Contact or Note from the address book or notebook"""
        self.__choose_entity(
            "Who should I delete?",
            self.delete_entity,
            self.__delete_contact,
            self.__delete_note
        )

    @keyboard_interrupt_handler
    def edit_entity(self):
        """Edits Contact or Note in the address book or notebook"""
        self.__choose_entity(
            "Who should I edit?",
            self.edit_entity,
            self.__edit_contact,
            self.__edit_note
        )

    @keyboard_interrupt_handler
    def search_entity(self):
        """Searches Contact or Note in the address book or notebook"""
        self.__choose_entity(
            "Who should I search?",
            self.search_entity,
            self.__search_contact,
            self.__search_note
        )

    @keyboard_interrupt_handler
    def show_birthdays(self):
        """Shows all contacts with for the next days_to_look_ahead days in the address book"""
        def enter_days():
            days = str(ConsolePrompt("Enter the number of days to look ahead"))
            if not days.isdigit():
                ErrorPanel("Invalid number of days", "Number of days must be a positive integer").show()
                enter_days()
            else:
                return int(days)
        days_to_look_ahead = enter_days()
        birthdays = self.__address_book.get_birthdays(days_to_look_ahead)
        birthdays_table = ConsoleTable("Birthdays", ["Name", "Surname", "Birthday"])
        for contact in birthdays:
            birthdays_table.add_row([contact.name, contact.surname, contact.birthday.strftime("%Y/%m/%d")])

    def _exit(self):
        choice = self.__confirm("Do you want to exit?")
        if choice:
            save_entities = self.__confirm("Do you want to save the address book and notebook?")
            if not save_entities:
                self.save_entities = False
            sys.exit(0)
        else:
            return

    @keyboard_interrupt_handler
    def exit(self):
        """Exits the Adviser"""
        self._exit()

    @keyboard_interrupt_handler
    def help(self):
        """Lists all commands available in the Adviser"""
        help_table = ConsoleTable("All Commands", ["Command", "Description"])
        for command in self.command_map:
            help_table.add_row([command, getattr(self, self.command_map[command]).__doc__])

        help_table.show()

    @keyboard_interrupt_handler
    def clear_saved_data(self):
        """Deletes the address book and notebook databases"""
        choice = self.__confirm("Do you want to delete the address book and notebook databases?")
        if choice:
            ADDRESS_BOOK_PATH.unlink(missing_ok=True)
            NOTEBOOK_PATH.unlink(missing_ok=True)
            InfoPanel("Database cleared", "Database cleared successfully").show()
        else:
            return

    def __del__(self):
        """Saves the address book and notebook to disk"""
        if self.save_entities:
            self.__notebook.save()
            self.__address_book.save()


