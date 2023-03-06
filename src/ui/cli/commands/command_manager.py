from src.manager import Manager

_module = "src.ui.cli.commands"
_commands = [

]


class CommandManager(Manager):

    commands = {}

    @classmethod
    def _initialize(cls):
        for command in _commands:
            Command = cls._import_command(_module, command)
            cls.commands[command] = Command

    @classmethod
    def _finalize(cls):
        cls.commands = {}

    @staticmethod
    def _import_command(module, command):
        instance = f"<DUMMY {command}>"
        print(f"IMPORT COMMAND {module} {command} -> {instance}")
        return instance

