from dataclasses import dataclass

import tkinter as tk
import numpy as np
import PIL.ImageTk

from clusteredreclaiminglist import CRQPosTracker
from layoutconsts import SMALL_THUMB_PIXEL_LENGTH, LARGE_THUMB_PIXEL_LENGTH
import dummy
from pagebrowser.compoundgui import Thumbnail
from pagebrowser.docinfo import VitVDocInfo

@dataclass
class Page(CRQPosTracker):

    vitv_doc: VitVDocInfo 
    orig_prev: PIL.ImageTk.PhotoImage
    thumb: Thumbnail = Thumbnail(
        dummy.dummy_frame,
        None,
        "",
        lambda _: None
    )
    selected: bool = False
    blank: bool = False


        
    @staticmethod
    def blank_page() -> "Page":
        return Page(
            VitVDocInfo.blank(),
            blank=True
        )