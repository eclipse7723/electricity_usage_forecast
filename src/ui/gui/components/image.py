from PIL import ImageTk
from PIL import Image as PillowImage
import tkinter as tk


class Image(tk.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = kwargs["path"]
        self.image = None

    def render(self):
        image = PillowImage.open(self.path)
        tk_image = ImageTk.PhotoImage(image)
        self.image = tk_image
