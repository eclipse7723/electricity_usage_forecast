# period
DEFAULT_DAYS_PERIOD = 30

# tariff
DEFAULT_TARIFF_THRESHOLD = 100.0
DEFAULT_TARIFF_BELOW_PRICE = 0.9
DEFAULT_TARIFF_ABOVE_PRICE = 1.68

# device
DEFAULT_DEVICES_PATH = "res/devices.json"
DEFAULT_DEVICE_ICON_PATH = "res/icons/default.png"
DEFAULT_DEVICES_SAVE_PATH = "res/connected_devices.json"

# general
DEFAULT_INTERFACE = "cli"
_DEBUG = False

MANAGERS = [
    ("src.devices.device_manager", "DeviceManager"),
    ("src.ui.interface_manager", "InterfaceManager"),
    ("src.ui.cli.commands.command_manager", "CommandManager"),
]

