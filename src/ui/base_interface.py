from src.ui.controller import Controller
from src.exceptions.process import AlreadyRunningError, AlreadyStoppedError
import threading


class BaseInterface:

    def __init__(self, controller=Controller):
        self.controller = controller()
        self._running = False
        self._active = False

    def _set_params(self):
        return

    def _show_error(self, exception):
        """ notify user about error """
        raise NotImplementedError

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

    def _stop(self):
        """ stop interface (for example, remove all observers, etc.) """
        raise NotImplementedError

    def stop(self):
        if self.is_running() is False:
            raise AlreadyStoppedError(self.__class__.__name__)

        self._running = False
        self._stop()
        self._active = False

