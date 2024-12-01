from collections.abc import Callable
import tkinter as tk
from typing import Any


import PIL
import PIL.Image
import PIL.ImageTk

from layoutconsts import SMALL_THUMB_SIZE, SMALL_THUMB_PAD
from vitvbind import propagate_parent
import colorconsts as colconsts



class SmallThumbnail:

    def selected_appearance(self, selected: bool):
        if selected:
            self.thumb_centerer.config(bg=colconsts.SELECTED_COLOR)
            self.label.config(bg=colconsts.SELECTED_COLOR)
        else:
            self.thumb_centerer.config(bg=colconsts.NONSELECTED_COLOR)
            self.label.config(bg=colconsts.NONSELECTED_COLOR)

    def __init__(self, root, thumb_img: PIL.ImageTk.PhotoImage, label: str, on_click: Callable[["Thumbnail"], None]):
        # Check if the image dimensions match the expected thumbnail size
        if thumb_img.width() != SMALL_THUMB_SIZE or thumb_img.height() != SMALL_THUMB_SIZE:
            raise ValueError(f"{thumb_img.width()}x{thumb_img.height()} image passed instead of {SMALL_THUMB_SIZE}x{SMALL_THUMB_SIZE} image")
        
        # Create the main frame to hold the thumbnail
        self.frame = tk.Frame(root, width=SMALL_THUMB_SIZE + SMALL_THUMB_PAD, height=SMALL_THUMB_SIZE + SMALL_THUMB_PAD)
        self.frame.grid_propagate(False)  # Prevent the frame from resizing based on contents
        
        # Create a centerer frame for the thumbnail
        self.thumb_centerer = tk.Frame(self.frame, width=SMALL_THUMB_SIZE + SMALL_THUMB_PAD, height=SMALL_THUMB_SIZE)
        self.thumb_centerer.grid_propagate(False)  # Prevent this frame from resizing based on contents
        
        # Add the thumbnail label inside the centerer frame
        self.thumbnail = tk.Label(self.thumb_centerer, image=thumb_img, width=SMALL_THUMB_SIZE, height=SMALL_THUMB_SIZE)
        self.thumbnail.grid(row=0, column=0, sticky="nsew", padx = SMALL_THUMB_PAD // 2)
        
        # Configure grid weight to prevent thumbnail from expanding beyond size
        self.thumb_centerer.grid_rowconfigure(0, weight=0)
        self.thumb_centerer.grid_columnconfigure(0, weight=0)

        # Place the centerer frame inside the main frame
        self.thumb_centerer.grid(row=0, column=0, sticky="nsew", )
        
        # Create a label for the thumbnail description
        self.label = tk.Label(self.frame, text=label, height=SMALL_THUMB_PAD // 2, width=SMALL_THUMB_PAD + SMALL_THUMB_SIZE)
        self.label.grid(row=1, column=0, sticky="nsew")
        
        # Configure the row weight of the parent frame to handle resizing better
        self.frame.grid_rowconfigure(0, weight=0)  # Prevent it from resizing
        self.frame.grid_rowconfigure(1, weight=1)  # Allow the label to grow
        self.frame.grid_columnconfigure(0, weight=1)  # Allow the column to expand

        self.frame.bind("<Button-1>", lambda evt: on_click(self))

        for w in (self.thumb_centerer, self.thumbnail, self.label):
            w.bind("<Button-1>", lambda e: propagate_parent(e, "<Button-1>"))

        self.selected_appearance(False)
    
class Thumbnail:
    def __init__(self, root, thumb_img: PIL.ImageTk.PhotoImage, label: str, on_click: Callable[["Thumbnail"], None]):

        self.small_thumb = SmallThumbnail(root, thumb_img, label, on_click)
        