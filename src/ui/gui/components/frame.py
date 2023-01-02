import tkinter as tk


class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        self.name = kwargs["name"]
        self.__widgets = {}

    def create_widget(self, name, type_widget, **params):
        widget = type_widget(master=self, **params)
        widget.pack(pack=params.get("pack_side", tk.LEFT))
        self.add_widget(name, widget)
        return widget

    def add_widget(self, name, widget):
        if name in self.__widgets.keys():
            return False
        if widget in self.__widgets.values():
            return False
        self.__widgets[name] = widget
        return True

    def remove_widget(self, name):
        widget = self.__widgets.pop(name)
        widget.destroy()

    def remove_widgets(self):
        for widget in self.each_widget():
            widget.destroy()
        self.__widgets = {}

    def get_widget(self, name):
        return self.__widgets.get(name)

    def each_widget(self):
        for widget in self.__widgets.values():
            yield widget
