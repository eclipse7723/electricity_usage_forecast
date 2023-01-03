from src.App import App
from src.ui.interface_manager import InterfaceManager


def prepare_managers():
    from src.devices.device_manager import DeviceManager
    DeviceManager.create_devices()


if __name__ == "__main__":
    prepare_managers()

    interface = InterfaceManager.get_interface("cli")
    app = App(interface)

    app.run()
