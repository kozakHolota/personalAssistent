from ui_components.panels import InfoPanel
from ui_components.prompt import ConsolePrompt

def keyboard_interrupt_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeyboardInterrupt:
            self._exit()

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper