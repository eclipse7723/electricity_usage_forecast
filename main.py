from src.App import App
from src.ui.interface_manager import InterfaceManager
from src.settings import DEFAULT_INTERFACE, _DEBUG


def finalize():
    from src.utils import import_type
    from src.settings import MANAGERS

    for module, name in MANAGERS:
        manager = import_type(module, name)
        manager.finalize()

        if _DEBUG:
            print(f"{name} finalized")

    from src.event import EventCollection
    EventCollection.removeObservers()
    if _DEBUG:
        print(f"removed all observers")

    return True


if __name__ == "__main__":
    interface = InterfaceManager.get_interface(DEFAULT_INTERFACE)
    app = App(interface)
    app.EVENT_APP_FINALIZED.addObserver(finalize)

    app.run()
