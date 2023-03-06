def initialize():
    from src.utils import import_type
    from src.settings import MANAGERS

    try:
        import os
        import sys
        os.chdir(sys._MEIPASS)
    except AttributeError:
        pass

    for module, name in MANAGERS:
        manager = import_type(module, name)
        manager.initialize()

    return True


initialize()
