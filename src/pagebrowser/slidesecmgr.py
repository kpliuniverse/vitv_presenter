from dataclasses import dataclass


import sys
import tkinter as tk
from typing import Callable
import numpy as np
from numpy.typing import NDArray

import vitvstring
from appconsts import MAX_PAGE_SEC_NAME_LIMIT, DEFAULT_RECLAIM_SLOTS, SECTION_ARRAY_CLUSTER_SIZE
from idorder import IDOrder
from clusteredreclaiminglist import ClusteredReclaimingList, CRQPosTracker
from layoutconsts import SMALL_THUMB_PIXEL_LENGTH, LARGE_THUMB_PIXEL_LENGTH
from pagebrowser.slideclass import Slide


validate_section_name = vitvstring.create_consistent_size_int_tuple_from_string_callable(MAX_PAGE_SEC_NAME_LIMIT)



class PageSecInfo(CRQPosTracker):
    def __init__(self, section_name: str, blank=False):
        self.section_name_in_array: NDArray[np.int32]  = self.validate_section_name(section_name)
        self.range_start = 0
        self.range_end = 0
        self.is_blank = blank

    @staticmethod
    def blank():
        return PageSecInfo("", blank=True)




class PageSectionMgr:
    def __init__(self):
        self.pagesecinfo_array = ClusteredReclaimingList(
            reclaim_slots=DEFAULT_RECLAIM_SLOTS,
            cluster_size=SECTION_ARRAY_CLUSTER_SIZE,
            exact_type_size=sys.getsizeof(PageSecInfo.blank()),
            none_object_creation_call=PageSecInfo.blank
        )