from src.manager import Manager
from src.utils import import_type
from src.exceptions.ui import CLICommandAlreadyExist
from src.ui.cli.commands.base_command import BaseCommand


_module = "src.ui.cli.commands"
_commands = [
    ("devices.add_device", "CommandDeviceAdd"),
    ("devices.edit_device", "CommandDeviceEdit"),
    ("devices.load_devices", "CommandDeviceLoad"),
    ("devices.my_devices", "CommandMyDevices"),
    ("devices.remove_device", "CommandDeviceRemove"),
    ("devices.save_devices", "CommandDeviceSave"),
    ("devices.show_device", "CommandDeviceShow"),
    ("model.calculate", "CommandCalculate"),
    ("model.change_period", "CommandPeriodChange"),
    ("model.show_period", "CommandPeriodShow"),
    ("model.change_tariff", "CommandTariffChange"),
    ("model.show_tariff", "CommandTariffShow"),
    ("stop", "CommandStopInterface"),
]


class CommandManager(Manager):

    commands = {}

    @classmethod
    def create(cls, name, alias, description, func):
        command = CustomCommand()
        command.initialize(
            alias=alias,
            description=description,
            func=func
        )

        try:
            cls.add(name, command)
        except CLICommandAlreadyExist:
            command.finalize()
            command = None

        return command

    @classmethod
    def add(cls, name, command):
        if name in cls.commands:
            raise CLICommandAlreadyExist(name)
        cls.commands[name] = command

    @staticmethod
    def get(name):
        return CommandManager.commands.get(name)

    @staticmethod
    def all():
        return CommandManager.commands.values()

    @classmethod
    def _initialize(cls):
        for module, name in _commands:
            command = cls._import_command(module, name)
            if command is None:
                continue

            cls.add(name, command)

    @classmethod
    def _finalize(cls):
        for command in cls.all():
            command.finalize()
        cls.commands = {}

    @staticmethod
    def _import_command(module, name):
        Command = import_type(f"{_module}.{module}", name)

        print(f"IMPORT COMMAND {module} {name} -> {Command}")

        if Command is None:
            return None

        command = Command()
        if command.initialize() is False:
            command.finalize()
            return None

        return command


class CustomCommand(BaseCommand):

    def initialize(self, alias, description, func):
        self.alias = alias
        self.description = description
        self._func = func
        self._initialized = True

    def _activate(self, *args, **kwargs):
        return self._func()

    def _finalize(self):
        self._funct = None
        return True
