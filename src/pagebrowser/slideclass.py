from dataclasses import dataclass

import tkinter as tk
import numpy as np
import PIL.ImageTk

from clusteredreclaiminglist import CRQPosTracker
from layoutconsts import SMALL_THUMB_PIXEL_LENGTH, LARGE_THUMB_PIXEL_LENGTH
import dummy
from pagebrowser import vitvimage
from pagebrowser.compoundgui import Thumbnail
from pagebrowser.presinfo import VitVPresInfo
from pagebrowser.vitvimage import blank_img

@dataclass
class Slide(CRQPosTracker):

    vitv_presentation: VitVPresInfo 
    orig_prev_upload_id: int
    selected: bool = False
    blank: bool = False


        
    @staticmethod
    def blank_page() -> "Slide":
        return Slide(
            VitVPresInfo.blank(),
            orig_prev = None,
            blank=True
        )