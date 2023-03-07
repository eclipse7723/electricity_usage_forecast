from src.ui.cli.commands.command_manager import CommandManager
from src.ui.cli.components.colors import Colors
from src.settings import _DEBUG


class CommandTree:

    def __init__(self, interface):
        self._interface = interface
        self.commands = {}
        self.initialize()

    def initialize(self):
        self.add_command("show commands", "shows all available commands", self.show_commands)
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

    def add_command(self, alias, description, func):
        command_class_name = "Command"+"".join([w.title() for w in alias.split(" ")])

        command = CommandManager.create(
            name=command_class_name,
            alias=alias,
            description=description,
            func=func
        )

        if command is None:
            return False

        self.commands[command.alias] = command
        return True

    def show_commands(self):
        print("All available commands:")
        for command in self.commands.values():
            print(f"  {Colors.wrap('green', command.alias)} - {command.description}")
        print()
