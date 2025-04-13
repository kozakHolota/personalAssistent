from command_line_handler.command_line_handler import CommandLineHandler
from ui_components.panels import InfoPanel


def main():
    command_handler = CommandLineHandler()
    InfoPanel(
        "Welcome!",
        "Welcome to the Assistant command line interface\nType 'help' to list available commands"
    ).show()

    while True:
        command_handler.handle_command()

if __name__ == "__main__":
    main()