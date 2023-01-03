import tkinter as tk
from src.ui.gui.components.frame import Frame
from src.ui.gui.components.image import Image
from src.ui.gui.components.label import Label
from src.ui.gui.components.entry import Entry
from src.ui.gui.components.button import Button
from src.model.period import Period
from src.event import Event, EventCollection


fonts = {
    "default": ("Helvetica", 14, "regular"),
    "small": ("Helvetica", 10, "regular"),
    "title": ("Helvetica", 16, "bold")
}


class DeviceCard(Frame):

    EVENT_CLICK_ADD = Event("onDeviceCardClickedAdd")
    EVENT_CLICK_REMOVE = Event("onDeviceCardClickedRemove")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = kwargs["device"]
        self.icon = None

        self.create_content()

    def create_content(self):
        device = self.device

        # FRAME ICON

        icon_block = self.create_widget("icon_block", Frame, pack_side=tk.LEFT)
        self.icon = icon_block.create_widget("icon", Image, path=device.icon_path)

        # FRAME DETAILS

        details_block = self.create_widget("details_block", Frame, pack_side=tk.LEFT)
        details_block.create_widget("title", Label, text=device.name, font=fonts["title"])

        power_validator = self.register(self._validate_power)
        power_block = details_block.create_widget("power_block", Frame, pack_side=tk.TOP)
        power_block.create_widget("title", Label, text="Power (Watt): ", font=fonts["default"])
        power_block.create_widget("entry", Entry, width=20,
                                  validate="key", validatecommand=(power_validator, "%d", "%P", "%S"))

        days_validator = self.register(self._validate_days)
        days_block = details_block.create_widget("days_block", Frame, pack_side=tk.TOP)
        days_block.create_widget("title", Label, text="Usage days: ", font=fonts["default"])
        days_block.create_widget("entry", Entry, width=20,
                                 validate="key", validatecommand=(days_validator, "%d", "%P", "%S"))

        hours_validator = self.register(self._validate_hours)
        hours_block = details_block.create_widget("hours_block", Frame, pack_side=tk.TOP)
        hours_block.create_widget("title", Label, text="Usage days: ", font=fonts["default"])
        hours_block.create_widget("entry", Entry, width=20,
                                  validate="key", validatecommand=(hours_validator, "%d", "%P", "%S"))

        # FRAME AMOUNT

        amount_block = self.create_widget("amount_block", Frame, pack_side=tk.LEFT)
        amount_block.create_widget("add", Button, pack_side=tk.TOP, text="+", command=self._add)
        amount_block.create_widget("remove", Button, pack_side=tk.TOP, text="-", command=self._remove)
        amount_block.create_widget("amount", Label, pack_side=tk.TOP, text=f"Amount: {self.device.amount}", font=fonts["small"])

    # actions ------------------

    def _add(self):
        """ on click 'add' """
        DeviceCard.EVENT_CLICK_ADD(self)

    def _remove(self):
        """ on click 'remove' """
        DeviceCard.EVENT_CLICK_REMOVE(self)

    # callbacks ----------------

    def add_observers(self):
        EventCollection.addObserver("onDeviceAmountUpdate", self._cb_amount_change)
        EventCollection.addObserver("onDeviceIconChange", self._cb_amount_change)

    def _cb_amount_change(self, device):
        if device.identity != self.device.identity:
            return False

        amount = self.device.amount

        # set buttons state
        block = self.get_widget("amount_block")
        if amount > 0:
            block.get_widget("remove").configure(state=tk.ACTIVE)
        else:
            block.get_widget("remove").configure(state=tk.DISABLED)

        label = self.get_widget("amount_block").get_widget("amount")
        label.configure(text=f"Amount: {amount}")
        return False

    def _cb_icon_change(self, device, icon_path):
        if device.identity != self.device.identity:
            return False

        block = self.get_widget("icon_block")
        block.remove_widget("icon")
        self.icon = block.create_widget("icon", Image, path=icon_path)
        return False

    # validators ---------------

    def _validate_power(self, action, current_text, input_char):
        current_value = int(current_text)

        if action == "1":     # insert
            if input_char.isdigit() is False:
                return False

        self.device.set_watt(current_value)
        return True

    def _validate_days(self, action, current_text, input_char):
        current_value = int(current_text)

        if action == "1":     # insert
            if input_char.isdigit() is False:
                return False

            if int(current_text) > Period.get_days():
                return False

        self.device.set_usage_days(current_value)
        return True

    def _validate_hours(self, action, current_text, input_char):
        current_value = float(current_text)

        if action == "1":     # insert
            if input_char == "." and current_text.count(".") > 1:
                return False
            elif input_char.isdigit() is False:
                return False

            if current_value > 24.0:
                # hours must be between [0, 24]
                return False

        self.device.set_usage_day_hours(current_value)
        return True



