from src.exceptions.process import AlreadyRunningError, AlreadyStoppedError
from src.event import Event


class App:

    EVENT_APP_FINALIZED = Event("onAppFinalized")
    __instance = None

    def __new__(cls, interface, *args, **kwargs):
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

        self.interface.EVENT_STOP.addObserver(self._cb_interface_stop)
        self.interface.start()
        self._running = True

    def stop(self):
        if self._running is False:
            raise AlreadyStoppedError(self.__class__.__name__)

        if self.interface.is_running() is True:
            self.interface.stop()
        self._running = False

        self._finalize()

    def _finalize(self):
        App.EVENT_APP_FINALIZED()

    def _cb_interface_stop(self, alias):
        if alias == self.interface.alias:
            self.stop()
        return False
