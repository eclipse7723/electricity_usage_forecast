from src.ui.cli.commands.base_command import BaseCommand


class CommandDeviceShow(BaseCommand):

    def _activate(self, *args, **kwargs):
        my_devices = self._interface.my_devices

        identity = input("Identity: ").lower()

        if identity in my_devices:
            device = my_devices[identity]
            print(str(device))
        else:
            self._device_not_connected(identity)

    def _device_not_connected(self, identity):
        error_msg = f"Device with identity {identity!r} not found in connected devices"
        self._interface.show_error(error_msg)

    def _setup_params(self):
        self.alias = "show device"
        self.description = "shows details of selected connected device"
