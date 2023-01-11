class CommandsTree:

    def __init__(self):
        self.commands = {}

    def enter_command(self):
        pass

    def find_command(self, name):
        if name not in self.commands:
            return None

        command = self.commands[name]
        return command

