

from dataclasses import dataclass
from typing import Literal
import PIL.Image
import PIL.ImageTk



def blank_img(w: int, h: int):
    # Create a new blank image
    img = PIL.Image.new('RGB', (w, h), color=(0, 0, 0))
    return img




INTERNAL = ""
CREATE_IMAGETK_PHOTOIMAGE: Literal[0b00001] = 2^0
CREATE_REAL_IMAGE: Literal[0b00010] = 2^1

class VitVImageContainer:
    tk_image: PIL.ImageTk.PhotoImage = None
    real_image: PIL.Image = None
    original_path: str = INTERNAL

    def __init__(self, img_path, tasks = 0b0):
        self.original_path = img_path
        if (CREATE_IMAGETK_PHOTOIMAGE ^ tasks) == CREATE_IMAGETK_PHOTOIMAGE:
            # Open the image and convert it to a Tkinter-compatible image
            self.tk_image = PIL.ImageTk.PhotoImage(PIL.Image.open(img_path))
        if (CREATE_REAL_IMAGE ^ tasks) == CREATE_REAL_IMAGE:
            self.real_image = PIL.ImageTk.Image(PIL.Image.open(img_path))
            
    def get_imgtk_phimg(self) -> PIL.ImageTk.PhotoImage:
        if (out := self.tk_image):
            return out
        else:
            raise TypeError("This ImageContainer does not contain a ImageTk.PhotoImage counterpart")
        
    @staticmethod
    def contain_imgtk_phimg(path, img) -> "VitVImageContainer":
        out: VitVImageContainer = VitVImageContainer(path)
        out.tk_image = img
        return img
    
    