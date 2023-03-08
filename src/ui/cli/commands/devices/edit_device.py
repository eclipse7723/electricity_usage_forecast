from src.ui.cli.commands.base_command import BaseCommand, with_accept_message
from src.ui.cli.commands.command_manager import CommandManager


class CommandDeviceEdit(BaseCommand):

    @with_accept_message
    def _activate(self, *args, **kwargs):
        if len(self._interface.my_devices) == 0:
            self._no_connected_devices()
            return

        identity = input("Device identity: ").lower()
        if identity not in self._interface.my_devices:
            self._device_not_connected(identity)
            return

        card = self._interface.my_devices[identity]
        card.edit()
        return True

    def _no_connected_devices(self):
        add_device_command = CommandManager.get("CommandDeviceAdd")

        self._interface.show_error(f"Connect at least one device. Type '{add_device_command.alias}'!")

    def _device_not_connected(self, identity):
        my_devices_command = CommandManager.get("CommandMyDevices")

        error_msg = f"Device with identity {identity!r} not connected. " \
                    f"Type '{my_devices_command.alias}' to view identities of your connected devices."
        self._interface.show_error(error_msg)

    def _setup_params(self):
        self.alias = "edit device"
        self.description = f"edit my connected device"
