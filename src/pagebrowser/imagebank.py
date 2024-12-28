import sys
from typing import Dict

from clusteredreclaiminglist import ClusteredReclaimingList
from pagebrowser.vitvimage import VitVImageContainer


class ImageBank:
    def __init__(self):
        self.deleted_image_slots = ClusteredReclaimingList(reclaim_slots=5, cluster_size=3, exact_type_size=sys.getsize(int()), none_object_creation_call=lambda: -1)
        self.images: Dict[int, VitVImageContainer] = {}

    def upload(self, img: VitVImageContainer) -> int:
        if (self.deleted_image_slots.length != 0):
            cur_id = self.deleted_image_slots.pop()
        else:
            cur_id = len(self.images)
        self.images[cur_id] = img

    def get(self, id: int) -> VitVImageContainer:
        out = self.images.get(id, None)
        if out is None:
            raise ValueError(f"No image with id {id} found.")
        return out
