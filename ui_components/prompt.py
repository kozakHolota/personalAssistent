from typing import List

from rich.prompt import Prompt


class ConsolePrompt:
    def __init__(self, prompt: str, choices: List[str] = None, default: str = None):
        self.default = default
        self.choices = choices
        self.prompt = prompt

    def __str__(self):
        return Prompt.ask(self.prompt, choices=self.choices, default=self.default)