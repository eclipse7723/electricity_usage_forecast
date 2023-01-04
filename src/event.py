import warnings


class EventCollection:
    events = {}
    observers = {}

    @staticmethod
    def get(name):
        return EventCollection.events.get(name)

    @staticmethod
    def addObserver(name, fn, *args, **kwargs):
        event = EventCollection.get(name)
        functor = event.addObserver(fn, *args, **kwargs)
        return functor

    @staticmethod
    def removeObservers():
        for event in EventCollection.events.values():
            event.removeObservers()

    @staticmethod
    def removeObserver(observer):
        if observer is None:
            return

        owner = observer.identity
        event = EventCollection.get(owner)
        event.removeObserver(observer)


class Event:

    def __init__(self, name):
        self.name = name
        self.observers = []
        EventCollection.events[name] = self

    def addObserver(self, fn, *args, **kwargs):
        observer = Observer(self.name, fn, *args, **kwargs)
        self.observers.append(observer)
        return observer

    def removeObservers(self):
        self.observers = []

    def removeObserver(self, observer):
        if observer not in self.observers:
            return
        self.observers.remove(observer)

    def __call__(self, *args, **kwargs):
        # print(f"* {self.name} {args} {kwargs}")

        for observer in self.observers:
            val = observer(*args, **kwargs)

            if val is False:
                continue

            if val is not True:
                warnings.warn(f"Event {self.name} should return boolean value")
            self.removeObserver(observer)


class Observer:
    def __init__(self, identity, fn, *args, **kwargs):
        self.identity = identity
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *_args, **_kwargs):
        args = self.args
        kwargs = self.kwargs.copy()

        if len(_args) > 0:
            args = _args + args
        if len(_kwargs) > 0:
            kwargs.update(_kwargs)

        if len(args) > 0 and len(kwargs) == 0:
            return self.fn(*args)
        elif len(args) > 0 and len(kwargs) > 0:
            return self.fn(*args, **kwargs)
        elif len(args) == 0 and len(kwargs) > 0:
            return self.fn(**kwargs)
        elif len(args) == 0 and len(kwargs) == 0:
            return self.fn()
