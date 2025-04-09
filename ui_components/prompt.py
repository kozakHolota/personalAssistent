from typing import List

from rich.prompt import Prompt


class ConsolePrompt:
    def __init__(self, prompt: str, choices: List[str] = None):
        self.choices = choices
        self.prompt = prompt

    def __str__(self):
        return Prompt.ask(self.prompt) if not self.choices \
            else Prompt.ask(self.prompt, choices=self.choices)