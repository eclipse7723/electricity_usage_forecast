from src.App import App
from src.ui.interface_manager import InterfaceManager


if __name__ == "__main__":
    interface = InterfaceManager.get_interface("gui")
    app = App(interface)

    app.run()
