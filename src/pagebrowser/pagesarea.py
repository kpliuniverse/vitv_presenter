import tkinter as tk
    

class PagesArea():

    def __init__(self, pages_area_frame_root: tk.Frame):
        self.frame = tk.Frame(pages_area_frame_root, bg="red")
        self.pack = self.frame.pack

    