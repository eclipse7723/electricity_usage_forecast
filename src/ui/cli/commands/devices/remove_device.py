from src.ui.cli.commands.base_command import BaseCommand, with_accept_message
from src.ui.cli.components.colors import Colors
from src.ui.cli.commands.command_manager import CommandManager


class CommandDeviceRemove(BaseCommand):

    def _setup_params(self):
        self.alias = "remove device"
        self.description = "disconnect device"

    @with_accept_message
    def _activate(self, *args, **kwargs):
        connected_devices = self._interface.controller.get_connected_devices()
        connected_devices = [device.identity for device in connected_devices]

        if len(connected_devices) == 0:
            self._not_found_connected_devices()
            return

        self._interface.show_tip("Type identities, separated with comma")
        identities = input("Identities: ").lower()

        at_least_one_disconnected = False
        for identity in identities.split(", "):
            if identity not in connected_devices:
                self._device_not_connected(identity)
                return

            self._interface.controller.disconnect_device(identity)
            at_least_one_disconnected = True

        return at_least_one_disconnected

    def _device_not_connected(self, identity):
        my_devices_command = CommandManager.get("CommandMyDevices")

        error_msg = f"Device with id {identity!r} not found in connected devices" \
                    f" - type '{my_devices_command.alias}' to check"
        self._interface.show_error(error_msg)

    def _not_found_connected_devices(self):
        add_device_command = CommandManager.get("CommandDeviceAdd")

        Colors.print("yellow", "No devices to disconnect :(")
        self._interface.show_tip(f"Type '{add_device_command.alias}' to connect a new device!")
