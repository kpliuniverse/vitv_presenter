import tkinter as tk
from tkinter import ttk
import PIL
import PIL.IcnsImagePlugin
import PIL.Image
import PIL.ImageTk

import layoutconsts
from compoundgui import SmallThumbnail, Thumbnail
import colorconsts
from pagesarea import PagesArea



    

#sample_image : PIL.Image = obtain_sample_img()
  


class MainApp:
    main_win: tk.Tk = tk.Tk()
    menu_bar: tk.Menu
    tool_bar: tk.Frame 
    pages_area_frame: tk.Frame
    pages_area_class: PagesArea

    menus: dict[str, tk.Menu] = dict()

    menu_cascades_table = (
        ("FILE", "File"),
        ("ABOUT", "About"),
        {"TEST", "Test"}
    )

    def file_menu(self):
        self.menus["FILE"].add_command(label="Load", command=None)
        self.menus["FILE"].add_command(label="Save", command=None)
        self.menus["FILE"].add_command(label="Save as", command=None)
        self.menus["FILE"].add_command(label="Quit", command=None)

    def init_menus(self):
        for menu_cascade in self.menu_cascades_table:
            self.menus[menu_cascade[0]] = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label = menu_cascade[1], menu = self.menus[menu_cascade[0]])
        self.file_menu()
        self.menus["ABOUT"].add_command(label = "About this software", command = None)
        self.menus["TEST"].add_command(label = "Open sample program via launcher")

    def init_pagebrowser(self):
        self.main_paned_win = ttk.PanedWindow(self.pages_area_frame, orient=tk.HORIZONTAL)
        self.pages_pane = tk.Frame(self.main_paned_win, bg=colorconsts.BG_COLOR)
        self.pages_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_paned_win.add(self.pages_pane, weight=3)
        self.preview_pane = tk.Frame(self.main_paned_win, bg="magenta")
        self.preview_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_paned_win.add(self.preview_pane, weight=2)
        self.main_paned_win.pack(fill=tk.BOTH, expand=True)
        self.pages_area_class = PagesArea(self.pages_pane)
        self.pages_area_class.pack(fill=tk.BOTH, expand=True)

    def select(self, thumb: SmallThumbnail):
        thumb.selected_appearance(True)



    def __init__(self):
        path: str = "assets/sampprev.png" 
        self.test_thumb_img: PIL.Image.Image
        with PIL.Image.open(path) as img:
            img = img.resize((layoutconsts.SMALL_THUMB_SIZE, layoutconsts.SMALL_THUMB_SIZE), PIL.Image.Resampling.LANCZOS)
            self.s_img = PIL.ImageTk.PhotoImage(img)
        self.main_win.geometry("1600x900")
        self.menu_bar =  tk.Menu(self.main_win)
        self.init_menus()
        
        self.main_win.config(menu=self.menu_bar, pady = int(layoutconsts.MENU_BAR_PAD))
        self.tool_bar = tk.Frame(self.main_win, height = int(layoutconsts.TOOLBAR_HEIGHT), bg="blue")
        self.tool_bar.grid(row=0, column=0, sticky = "new")
        self.pages_area_frame =  tk.Frame(self.main_win)
        self.pages_area_frame.grid(row=1, column=0, sticky = "nsew")
        self.main_win.columnconfigure(0, weight=1)
        self.main_win.rowconfigure(0, weight=0)
        self.main_win.rowconfigure(1, weight=1)

        self.init_pagebrowser()

        
        
    def run(self): 
        self.main_win.mainloop()
        