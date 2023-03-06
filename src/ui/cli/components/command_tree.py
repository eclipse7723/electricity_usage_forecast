from src.ui.cli.commands.command_manager import CommandManager
from src.ui.cli.components.colors import Colors
from src.settings import _DEBUG


class CommandTree:

    def __init__(self, interface):
        self._interface = interface
        self.commands = {}
        self.initialize()

    def initialize(self):
        for command in CommandManager.all():
            command.set_interface(self._interface)
            self.commands[command.alias] = command

    def finalize(self):
        for command in self.commands.values():
            command.finalize()
        self.commands = {}

    def enter(self):
        name = input("> ").lower()

        if len(name) == 0:
            # ignore
            return

        command = self.find_command(name)
        if command is None:
            self._interface.show_error(f"Command {name!r} not found")
            self.show_commands()
            return

        if _DEBUG is True:
            command()
        else:
            try:
                command()
            except Exception as e:
                self._interface.show_error(f"{e.__class__.__name__}: {str(e)}")

    def find_command(self, name):
        if name not in self.commands:
            return None

        command = self.commands[name]
        return command

    def show_commands(self):
        print("All available commands:")
        for command in self.commands.values():
            print(f"  {Colors.wrap('green', command.alias)} - {command.description}")
        print()
