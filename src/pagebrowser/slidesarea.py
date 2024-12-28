import tkinter as tk

import PIL.ImageTk

from compoundgui import Thumbnail
from layoutconsts import SMALL_THUMB_SIZE, SMALL_THUMB_PAD, MIN_SLIDES_AREA_WIDTH, THUMBS_PADY
import colorconsts
from testdummies import random_dummy_image
from vitvimage import blank_img

class SlidesArea():

    how_many_thumbs_fit_along_x: int 
    last_how_many_thumbs_fit_along_x: int = -1
    cur_thumb_size: int = SMALL_THUMB_SIZE
    cur_thumb_pad: int = SMALL_THUMB_PAD
    extra_space_dist: int
    inited: bool = False

    def calc_how_many_thumbs_fit_along_x(self):
        total_thumb_size = self.cur_thumb_size + self.cur_thumb_pad
        self.how_many_thumbs_fit_along_x = self.frame.winfo_width() // total_thumb_size
        extra_space = self.frame.winfo_width() - self.how_many_thumbs_fit_along_x * total_thumb_size
        self.extra_space_dist = extra_space // self.how_many_thumbs_fit_along_x
        

    def refresh(self):
        #self.frame.config(padx=self.extra_space_dist)
        for i, th in enumerate(self.thumbnails):
            th.small_thumb.frame.grid(row=i // self.how_many_thumbs_fit_along_x, column=i % self.how_many_thumbs_fit_along_x, padx=self.extra_space_dist // 2, pady=THUMBS_PADY // 2)
    
    def on_resizex(self):
        if(self.frame.winfo_width() < MIN_SLIDES_AREA_WIDTH):
            return
        self.calc_how_many_thumbs_fit_along_x()
        if (self.how_many_thumbs_fit_along_x < 1):
            return
        #if (self.how_many_thumbs_fit_along_x == self.last_how_many_thumbs_fit_along_x):
            #return
        self.refresh()
        self.last_how_many_thumbs_fit_along_x = self.how_many_thumbs_fit_along_x
    def on_resize(self, evt):
        #print("ag")
        self.on_resizex()
    def __init__(self, pages_area_frame_root: tk.Frame):
        self.frame = tk.Frame(pages_area_frame_root, bg=colorconsts.BG_COLOR)
        self.pack = self.frame.pack
        self.thumbnails: list[Thumbnail] = []
        self.frame.bind("<Configure>", self.on_resize)

        for i in range(10):
            c = random_dummy_image((SMALL_THUMB_SIZE, SMALL_THUMB_SIZE))
            thumb = Thumbnail(self.frame, PIL.ImageTk.PhotoImage(c), f"Test thumb {i}", lambda x: None)
            self.thumbnails.append(thumb)

        

    def first_calc(self):
        self.frame.update_idletasks()
        self.calc_how_many_thumbs_fit_along_x()
        self.refresh()
        self.inited = True


    