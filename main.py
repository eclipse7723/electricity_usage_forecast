from src.App import App
from src.ui.interface_manager import InterfaceManager
from src.settings import DEFAULT_INTERFACE


def finalize():
    from src.utils import import_type
    from src.settings import MANAGERS

    for module, name in MANAGERS:
        manager = import_type(module, name)
        manager.finalize()

    from src.event import EventCollection
    EventCollection.removeObservers()
    return True


if __name__ == "__main__":
    interface = InterfaceManager.get_interface(DEFAULT_INTERFACE)
    app = App(interface)
    app.EVENT_APP_FINALIZED.addObserver(finalize)

    app.run()
