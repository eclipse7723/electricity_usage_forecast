from src.manager import Manager
from src.exceptions.ui import *
from src.ui.gui.graphic_interface import GraphicInterface
from src.ui.cli.command_line import CommandLineInterface


class InterfaceManager(Manager):
    interfaces = {
        GraphicInterface.alias: GraphicInterface,           # tkinter
        CommandLineInterface.alias: CommandLineInterface    # command line
    }

    @classmethod
    def _finalize(cls):
        cls.interfaces = {}

    @staticmethod
    def has_interface(name):
        return name in InterfaceManager.interfaces

    @staticmethod
    def get_interface(name):
        if InterfaceManager.has_interface(name) is False:
            raise InterfaceNotFoundError(name)
        interface = InterfaceManager.interfaces[name]
        return interface
