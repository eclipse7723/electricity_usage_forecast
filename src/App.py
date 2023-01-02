from src.exceptions.process import AlreadyRunningError, AlreadyStoppedError


class App:

    __instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton pattern
        if App.__instance is None:
            App.__instance = super().__new__(cls, *args, **kwargs)
        return App.__instance

    def __init__(self, interface):
        self.interface = interface()
        self._running = False

    def run(self):
        if self._running is True:
            raise AlreadyRunningError(self.__class__.__name__)

        self.interface.start()
        self._running = True

    def stop(self):
        if self._running is True:
            raise AlreadyStoppedError(self.__class__.__name__)

        self.interface.stop()
        self._running = False
