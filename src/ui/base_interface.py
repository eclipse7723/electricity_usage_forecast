from src.ui.controller import Controller
from src.exceptions.process import AlreadyRunningError, AlreadyStoppedError
from src.event import Event, EventCollection
import threading


class BaseInterface:

    alias = None

    EVENT_START = Event("onInterfaceStart")
    EVENT_STOP = Event("onInterfaceStop")

    def __init__(self, controller=Controller):
        self.controller = controller()
        self._running = False
        self._active = False
        self.__observers = []

    def _set_params(self):
        return

    def show_error(self, exception):
        """ notify user about error """
        raise NotImplementedError

    # utils

    def _add_observer(self, name, cb):
        self.__observers.append(EventCollection.addObserver(name, cb))

    def _remove_observers(self):
        for observer in self.__observers:
            EventCollection.removeObserver(observer)
        self.__observers = []

    # interface flow

    def is_running(self):
        """ when we just set params, before `prepare` """
        return self._running is True

    def is_active(self):
        """ when interface actually done all prepare, start things """
        return self._active is True

    def _prepare(self):
        return

    def _start(self):
        """ start interface (for example, create buttons, bind them, etc) """
        raise NotImplementedError

    def start(self):
        if self.is_running() is True:
            raise AlreadyRunningError(self.__class__.__name__)

        self._set_params()
        self._running = True
        self._prepare()
        threading.Thread(target=self._start).start()
        self._active = True

        self.EVENT_START(self.alias)

    def _stop(self):
        """ stop interface (for example, remove all observers, etc.) """
        raise NotImplementedError

    def stop(self):
        if self.is_running() is False:
            raise AlreadyStoppedError(self.__class__.__name__)

        self._running = False
        self._stop()
        self._remove_observers()
        self._active = False

        self.EVENT_STOP(self.alias)

