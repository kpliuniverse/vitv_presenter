import sys
from clusteredreclaiminglist import ClusteredReclaimingList
from pagebrowser.pageclass import Page
from pagebrowser.pagesecmgr import PageSectionMgr
import vitvstring
import appconsts
from pagebrowser.docinfo import VitVDocInfo


class VitVDocument:
    page_array = ClusteredReclaimingList(
        reclaim_slots=appconsts.DEFAULT_RECLAIM_SLOTS,
        cluster_size=appconsts.SECTION_ARRAY_CLUSTER_SIZE,
        exact_type_size=sys.getsizeof(Page.blank_page()),
        none_object_creation_call=Page.blank_page
    )
    doc_info: VitVDocInfo
    pagesec_mgr: PageSectionMgr = PageSectionMgr()
    def __init__(self, width: int, height: int):
        self.doc_info = VitVDocInfo(
            width=width,
            height=height
        )
    
    