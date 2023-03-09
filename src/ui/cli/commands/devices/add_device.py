from src.ui.cli.commands.base_command import BaseCommand, with_accept_message
from src.ui.cli.components.colors import Colors


class CommandDeviceAdd(BaseCommand):

    def _setup_params(self):
        self.alias = "add device"
        self.description = "connect a new device"

    @with_accept_message
    def _activate(self, *args, **kwargs):
        not_connected_devices = self._interface.controller.get_not_connected_devices()

        if len(not_connected_devices) == 0:
            Colors.print("yellow", "No devices to connect :(")
            return

        self._interface.show_tip("List of not connected devices:")
        for device in not_connected_devices:
            print(f" [{Colors.wrap('yellow', device.identity)}] {device.name!r} ({device.power} Watt)")
        self._interface.show_tip("Type identities from square brackets to add device, separated with comma")

        identities = input("Identities: ").lower()
        if len(identities) == 0:
            return

        at_least_one_connected = False
        for identity in identities.split(", "):
            if identity not in [device.identity for device in not_connected_devices]:
                self._interface.show_error(f"Device with id '{identity}' not found")
                continue
            self._interface.controller.connect_device(identity)
            at_least_one_connected = True

        return at_least_one_connected
