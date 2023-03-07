from src.exceptions.ui import CLICommandNotInitialized
from src.ui.cli.components.colors import Colors


def with_accept_message(func):
    def _wrapper(*args, **kwargs):
        if func(*args, **kwargs) is True:
            Colors.print("green", "Your changes has been accepted!")

    return _wrapper


class BaseCommand:

    def __init__(self):
        self.alias = self.__class__.__name__
        self.description = f"{self.__class__.__name__} - default description"
        self._interface = None
        self._initialized = False

    def __call__(self, *args, **kwargs):
        if self._initialized is False:
            raise CLICommandNotInitialized(self)
        return self._activate(*args, **kwargs)

    def set_interface(self, interface):
        self._interface = interface

    def initialize(self, **kwargs):
        self._setup_params()
        self._initialize()

        if self.test() is False:
            return False

        self._initialized = True
        return True

    def finalize(self):
        self._finalize()
        self._interface = None
        self._initialized = False

    def test(self):
        return self._test()

    def _initialize(self):
        return True

    def _finalize(self):
        return True

    def _activate(self, *args, **kwargs):
        """ when command activates, must return bool """
        raise NotImplementedError

    def _test(self):
        """ test command here - should raise exception if failed, or return bool """
        return True

    def _setup_params(self):
        """ add new attrs here """
        return
