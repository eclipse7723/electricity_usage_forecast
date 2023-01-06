from src.ui.base_interface import BaseInterface
from src.event import EventCollection

from src.ui.gui.components.frame import Frame
from src.ui.gui.components.entry import Entry
from src.ui.gui.components.button import Button
from src.ui.gui.components.label import Label

from src.ui.gui.blocks.device_card import DeviceCard
from src.ui.gui.blocks.scroll_frame import HorizontalScrollFrame

import tkinter as tk


class GraphicInterface(BaseInterface, tk.Tk):

    alias = "gui"

    width = 440
    height = 310

    def _set_params(self):
        self.layers = {}

    def _prepare(self):
        self.title("Electricity usage forecast")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.create_content()
        self.add_observers()

    def _start(self):
        pass

    def _stop(self):
        for frame in self.layers.values():
            frame.remove_widgets()
        self.destroy()

    # LAYOUT ------------------------------------------

    def create_layer(self, name, frame_type=Frame, **params):
        frame = frame_type(name=name, **params)
        self.layers[frame.name] = frame
        return frame

    def create_content(self):
        # tariff and period params
        self._create_tariff_period_layer()

        # connected_devices layer
        self._create_connected_devices_layer()

        # calc layer
        self._create_calculate_layer()

        # results layer
        self._create_results_layer()

    def _create_tariff_period_layer(self):
        layer = self.create_layer("tariff_period")
        layer.pack(side=tk.TOP, fill=tk.X)

        validator1 = self.register(self._validate_positive_float)
        tariff_block = layer.create_widget("tariff", Frame, pack_side=tk.TOP)
        tariff_block.create_widget("title", Label, text="Tariff (price per used kWh) with threshold")
        tariff_block.create_widget("below_th_entry", Entry,
                                   validate="key", validatecommand=(validator1, "%d", "%P", "%S"))
        tariff_block.create_widget("sep1", Label, text=" / ")
        tariff_block.create_widget("threshold", Entry,
                                   validate="key", validatecommand=(validator1, "%d", "%P", "%S"))
        tariff_block.create_widget("sep2", Label, text=" / ")
        tariff_block.create_widget("above_th_entry", Entry,
                                   validate="key", validatecommand=(validator1, "%d", "%P", "%S"))

        validator2 = self.register(self._validate_positive_integer)
        period_block = layer.create_widget("period", Frame, pack_side=tk.TOP)
        period_block.create_widget("label", Label, text="Period (in days)")
        period_block.create_widget("entry", Entry, validate="key", validatecommand=(validator2, "%d", "%S"))

    def _create_connected_devices_layer(self):
        layer = self.create_layer("connected_devices", frame_type=HorizontalScrollFrame)
        layer.pack(side=tk.TOP, fill=tk.X)

        for device in self.controller.get_connected_devices():
            self.__add_connected_device(device)

    def __add_connected_device(self, device):
        layer = self.layers["connected_devices"]

        card = DeviceCard(device=device)
        layer.add_widget(device.identity, card)
        card.pack(side=tk.TOP)

    def __remove_connected_device(self, device):
        layer = self.layers["connected_devices"]
        layer.remove_widget(device.identity)

    def _create_calculate_layer(self):
        layer = self.create_layer("calculate")

        button = layer.create_widget("calculate", Button)

    def _create_results_layer(self):
        layer = self.create_layer("results")

        res_energy = layer.create_widget("energy_results", Label)
        res_price = layer.create_widget("price_results", Label)

    # VALIDATORS -----------------------------------------------------------

    def _validate_positive_float(self, action, current_text, input_char):
        if action == "1":     # insert
            if input_char == "." and current_text.count(".") > 1:
                return False
            elif input_char.isdigit() is False:
                return False
        return True

    def _validate_positive_integer(self, action, input_char):
        if action == "1":     # insert
            if input_char.isdigit() is False:
                return False
        return True

    # CALLBACKS ------------------------------------------------------------

    def add_observers(self):
        EventCollection.addObserver("onDeviceCardClickedAdd", self._cb_device_clicked_increase)
        EventCollection.addObserver("onDeviceCardClickedRemove", self._cb_device_clicked_decrease)

    def _cb_device_clicked_increase(self, device_card):
        identity = device_card.device.identity
        self.controller.increase_device_amount(identity)
        return False

    def _cb_device_clicked_decrease(self, device_card):
        identity = device_card.device.identity
        self.controller.decrease_device_amount(identity)
        return False

    # REACTIONS ------------------------------------------------------------

    def _show_error(self, exception):
        print("[!!!!]" + str(exception))


