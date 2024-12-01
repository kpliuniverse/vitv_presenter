from dataclasses import dataclass
import sys
from clusteredreclaiminglist import ClusteredReclaimingList, CRQPosTracker

@dataclass
class Anon(CRQPosTracker):
    id: int
    active: bool


def create_none_anon():
    return Anon(0, False)


if __name__ == "__main__": 
    cq: ClusteredReclaimingList = ClusteredReclaimingList(
        reclaim_slots=3, 
        cluster_size=6, 
        exact_type_size=sys.getsizeof(create_none_anon()), 
        none_object_creation_call=create_none_anon
    )
    

    cq.push(Anon(1, True))
    cq.push(Anon(2, True))
    cq.push(Anon(3, False))
    cq.push(Anon(4, True))
    cq.push(Anon(5, True))
    cq.push(Anon(6, False))
    cq.push(Anon(7, False))
    cq.push(Anon(8, False))
    cq.push(Anon(9, True))
    cq.push(Anon(10, False))
    cq.push(Anon(11, False))
    cq.remove(3)
    cq.remove(4)
    cq.remove(5)
    cq.remove(5)
    cq.push(Anon(12, False))
    cq.push(Anon(13, True))
    cq.push(Anon(14, False))
    cq.push(Anon(15, True))
    cq.insert(Anon(16, False), 1)
    cq.insert(Anon(17, False), 0)
    cq.swap(5, 12)
    cq.swap(11, 12)
    cq.move(12, 0)
    for n, i in enumerate(cq):
        print(f"{n}: {i}")
    

    print("what")