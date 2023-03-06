from src.manager import Manager
from src.utils import import_type


_module = "src.ui.cli.commands"
_commands = [
    ("devices.add_device", "CommandDeviceAdd"),
    ("devices.edit_device", "CommandDeviceEdit"),
    ("devices.load_device", "CommandDeviceLoad"),
    ("devices.my_devices", "CommandMyDevices"),
    ("devices.remove_device", "CommandDeviceRemove"),
    ("devices.save_devices", "CommandDeviceSave"),
    ("devices.show_device", "CommandDeviceShow"),
    ("model.calculate", "CommandCalculate"),
    ("model.change_period", "CommandPeriodChange"),
    ("model.show_period", "CommandPeriodShow"),
    ("model.change_tariff", "CommandPeriodChange"),
    ("model.show_tariff", "CommandTariffShow"),
    ("stop", "CommandStopInterface"),
]


class CommandManager(Manager):

    commands = {}

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

            cls.commands[name] = command

    @classmethod
    def _finalize(cls):
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

