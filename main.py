from src.App import App
from src.ui.interface_manager import InterfaceManager
from src.settings import DEFAULT_INTERFACE, DEFAULT_DEVICES_PATH


def prepare_managers():
    from src.devices.device_manager import DeviceManager
    
    try:
        import os
        import sys
        os.chdir(sys._MEIPASS)
    except AttributeError:
        pass
    
    DeviceManager.create_devices()


if __name__ == "__main__":
    prepare_managers()

    interface = InterfaceManager.get_interface(DEFAULT_INTERFACE)
    app = App(interface)

    app.run()
