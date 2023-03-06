def import_type(module, name):
    Module = __import__(module, fromlist=[name])
    Type = getattr(Module, name)
    return Type
