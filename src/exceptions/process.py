class ProcessException(Exception):
    pass


class AlreadyRunningError(ProcessException):
    def __init__(self, process_name):
        exception_message = f"Process {process_name!r} is already run"
        super(AlreadyRunningError, self).__init__(exception_message)


class AlreadyStoppedError(ProcessException):
    def __init__(self, process_name):
        exception_message = f"Process {process_name!r} is already stop"
        super(AlreadyStoppedError, self).__init__(exception_message)
