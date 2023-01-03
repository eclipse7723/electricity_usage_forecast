import tkinter as tk
from src.ui.gui.components.frame import Frame


class _ScrollFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = None
        self.scroll = None
        self._width = kwargs.get("width", 100)
        self._height = kwargs.get("height", 100)

        self.create_content()

    def create_content(self):
        raise NotImplementedError("Please use `VerticalScrollFrame` or `HorizontalScrollFrame`")


class VerticalScrollFrame(_ScrollFrame):
    def create_content(self):
        canvas = tk.Canvas(self)
        self.canvas = canvas

        scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=self.canvas.yview)
        self.scroll = scroll

        canvas.config(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


class HorizontalScrollFrame(_ScrollFrame):
    def create_content(self):
        canvas = tk.Canvas(self)
        self.canvas = canvas

        scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        scroll.pack(side=tk.BOTTOM, fill=tk.X)
        scroll.config(command=self.canvas.xview)
        self.scroll = scroll

        canvas.config(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
