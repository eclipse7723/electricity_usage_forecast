from src.ui.base_interface import BaseInterface
from src.ui.gui.components.frame import Frame
from src.ui.gui.components.entry import Entry
from src.ui.gui.components.button import Button
from src.ui.gui.components.label import Label

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class GraphicInterface(BaseInterface, tk.Tk):

    def _set_params(self):
        self.layers = {}

    def _prepare(self):
        self.create_content()
        self.add_observers()

    def _start(self):
        pass

    def _stop(self):
        for frame in self.layers.values():
            frame.remove_widgets()

    # LAYOUT ------------------------------------------

    def create_layer(self, name, **params):
        frame = Frame(name=name, **params)
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

        tariff_label = layer.create_widget("tariff_label", Label)
        tariff_entry = layer.create_widget("tariff_entry", Entry)

        period_label = layer.create_widget("period_label", Label)
        period_entry = layer.create_widget("period_entry", Entry)

    def _create_connected_devices_layer(self):
        layer = self.create_layer("connected_devices")

        pass

    def _create_calculate_layer(self):
        layer = self.create_layer("calculate")

        button = layer.create_widget("calculate", Button)

    def _create_results_layer(self):
        layer = self.create_layer("results")

        res_energy = layer.create_widget("energy_results", Label)
        res_price = layer.create_widget("price_results", Label)

    # REACTIONS ------------------------------------------------------------

    def add_observers(self):
        pass


