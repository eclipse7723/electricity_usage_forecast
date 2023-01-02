import tkinter as tk
from src.ui.gui.components.frame import Frame
from src.ui.gui.components.image import Image
from src.ui.gui.components.label import Label
from src.ui.gui.components.entry import Entry


class DeviceCard(Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        device = kwargs["device"]
        self.device = device

        icon_block = self.create_widget("icon", Frame, pack_side=tk.LEFT)
        self.icon = icon_block.create_widget("icon", Image, path=device.icon_path)

        details_block = self.create_widget("details", Frame, pack_side=tk.TOP)
        details_block.create_widget("title", Label, text=device.name, font=("Helvetica", 16, "bold"))

        # TODO:

        # power
        # amount
        # usage days
        # usage hours

        # button (+)




