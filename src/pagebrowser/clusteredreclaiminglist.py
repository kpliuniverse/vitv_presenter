
from copy import deepcopy
from dataclasses import dataclass
import gc
import sys
from typing import Callable


@dataclass
class TableCoord:
    __slots__ = ['super_ind', 'sub_ind']
    super_ind: int
    sub_ind: int


    def shift_add(self, super_ind: int = 0, sub_ind: int = 0): 
        self.super_ind += super_ind
        self.sub_ind += sub_ind

        
    def override(self, super_ind: int = None, sub_ind: int = None):
        if super_ind is not None:
            self.super_ind = super_ind
        if sub_ind is not None:
            self.sub_ind = sub_ind

    def replace(self, replacement: "TableCoord"):
        self.super_ind = replacement.super_ind
        self.sub_ind = replacement.sub_ind

    @staticmethod
    def copy(x: "TableCoord") -> "TableCoord":
        return TableCoord(x.super_ind, x.sub_ind)
    

    @staticmethod
    def from_reclaim_coord(x: "ReclaimCoord") -> "TableCoord":
        return TableCoord(x.super_ind, x.sub_ind)

    

@dataclass
class ReclaimCoord(TableCoord):
    __slots__ = ['super_ind', 'sub_ind', "is_reclaim"]
    is_reclaim: False

    
    def clear(self):
        self.is_reclaim = False
        self.super_ind = 0
        self.sub_ind = 0

    @staticmethod
    def from_tablecoord(tablecoord: TableCoord, is_reclaim):
        return ReclaimCoord(tablecoord.super_ind, tablecoord.sub_ind, is_reclaim)
    
    def activate(self):
        self.is_reclaim = True

    @staticmethod
    def copy(x: "ReclaimCoord") -> "ReclaimCoord":
        return ReclaimCoord(x.super_ind, x.sub_ind, x.is_reclaim)

class CRQPosTracker:

    def crq_print(self):
        print(f"private_crq_coord: {self.private_crq_coord}")
        print(f"private_prev_coord: {self.private_prev_coord}")
        print(f"private_next_coord: {self.private_next_coord}")
    private_crq_coord: TableCoord = None
    private_prev_coord: TableCoord = None
    private_next_coord: TableCoord = None   



CRL_CHECK_INTERVAL: int = 5 
#WOW around 179 lines of code without testing
class ClusteredReclaimingList:
    #TODO LATER: auto delete empty rows
    #Complications:
    #       - Needs to delete reclaim_slots referencing row, and this causes holes, as the queue is expected to be continuous
    # Example situation: 
    # Reclaim Slot Rows: A, C, C, B, A, C, A, A, B, B
    # Delete row C
    # Reclaim Slot Rows: A, [], [], B, A, [], A, A, B, B
    # Might result in returning empty reclaim coordinates
    # Solution:
    #  clqsol.xlsx
    def print(self):
        print(f"length: {self.length}")
        print(f"cluster_size: {self.cluster_size}, exact_type_size: {self.exact_type_size}")
        print(f"none_object_creation_call: {self.none_object_creation_call}")
        print(f"reclaim_slots (length {self.reclaim_queue_len}/{self.reclaim_slots} max): {self.reclaim_queue}")
        print(f"has discarded a reclaim_slot = {self.discarded_reclaim_spot}")
        print(f"Contents:")
        for cluster in self.__table:
            print(cluster)

    def __init__ (self, reclaim_slots: int, cluster_size: int, exact_type_size: int, none_object_creation_call: Callable[[], object]):
        self.check_interval_cur = 0
        self.is_itering = False
        self.reclaim_slots =  reclaim_slots
        self.reclaim_queue: tuple[ReclaimCoord] = tuple(ReclaimCoord(0, 0, False) for _ in range(reclaim_slots))
        self.reclaim_queue_len = 0
        self.cluster_size: int = cluster_size
        self.none_object_creation_call = none_object_creation_call
        self.exact_type_size: int = exact_type_size
        self.__table: list[list[CRQPosTracker]] = [self.__return_empty_cluster(self.cluster_size)]
        
        self.last_nonfree_pos: TableCoord = TableCoord(0, 0)
        self.first_coord: TableCoord = TableCoord.copy(self.last_nonfree_pos)
        self.last_coord: TableCoord = TableCoord.copy(self.last_nonfree_pos)
        self.length = 0
        self.discarded_reclaim_spot = False
        self.earliest_discard: None | TableCoord = None
    def __iter__(self):
        self.is_itering = True
        cur_coord = self.first_coord
        for i in range(self.length):
            y = self.__fetch_w_coord(cur_coord)
            cur_coord = y.private_next_coord
            #y.crq_print()
            yield y
        self.is_itering = False


    def __return_empty_cluster(self, cluster_size: int) -> list:
        x = self.none_object_creation_call()
        assert sys.getsizeof(x) == self.exact_type_size
        return [x for _ in range(cluster_size)]

    def insert(self, item: CRQPosTracker, index: int):
        """
        Inserts an item into the collection at the specified index.
        
        Parameters:
        - item (CRQPosTracker): The item to be inserted into the collection.
        - index (int): The index at which to insert the item.
        
        Raises:
        - IndexError: If the index is out of range.
        - ValueError: If the item does not inherit from CRQPosTracker or if the size of the item is not the exact size specified.
        
        Returns:
        - None: The function does not return any value.
        """
        if self.is_itering:
            raise Exception("Cannot insert while iterating")
        if not isinstance(item, CRQPosTracker):
            raise ValueError (f"Object must inherit from CRQPosTracker. It seems {item} is not")
        if sys.getsizeof(item) != self.exact_type_size:
            raise ValueError (f"Object not the exact size as specified. {sys.getsizeof(item)}B sized appendage to collection {self.exact_type_size}B items ")
        if (self.last_nonfree_pos.super_ind == len(self.__table)):
            self.__table.append(self.__return_empty_cluster(self.cluster_size))
        if self.discarded_reclaim_spot and self.reclaim_queue_len == 0:
            self.__single_reclaim_add_from_find()
        coord_to_put: TableCoord = self.__get_free_coord()
        self.__place_w_coord(item, coord_to_put)
        item.private_crq_coord = TableCoord.copy(coord_to_put)
        if self.discarded_reclaim_spot and self.reclaim_queue_len == 0:
            self.__single_reclaim_add_from_find()
        if(index == 0) and (self.length > 1):
            item.private_next_coord = TableCoord.copy(self.first_coord)
            self.__fetch_w_coord(self.first_coord).private_prev_coord = TableCoord.copy(coord_to_put)
            item.private_next_coord = TableCoord.copy(self.first_coord)
            self.first_coord.replace(coord_to_put)
            self.length += 1
            return
        displace_coord = self.__index_to_tablecoord(index)
        displace_x = self.__fetch_w_coord(displace_coord)
        prev_displace_x = self.__fetch_w_coord(displace_x.private_prev_coord)
        item.private_next_coord = TableCoord.copy(displace_coord)
        item.private_prev_coord = TableCoord.copy(displace_x.private_prev_coord)
        displace_x.private_prev_coord.replace(coord_to_put)
        prev_displace_x.private_next_coord.replace(coord_to_put)
        self.length += 1

    def push(self, item: CRQPosTracker):
        if self.is_itering:
            raise ValueError("Cannot push an item while iterating")
        #TODO: dedicated copy static function of CRQPosTracker
        if not isinstance(item, CRQPosTracker):
            raise ValueError (f"Object must inherit from CRQPosTracker. It seems {item} is not")
        if sys.getsizeof(item) != self.exact_type_size:
            raise ValueError (f"Object not the exact size as specified. {sys.getsizeof(item)}B sized appendage to collection {self.exact_type_size}B items ")
        if (self.last_nonfree_pos.super_ind == len(self.__table)):
            self.__table.append(self.__return_empty_cluster(self.cluster_size))
        if self.discarded_reclaim_spot and self.reclaim_queue_len == 0:
            self.__single_reclaim_add_from_find()
        
        coord_to_put: TableCoord = self.__get_free_coord()
        
        self.__place_w_coord(item, coord_to_put)
        item.private_crq_coord = coord_to_put
        
        if (self.length == 0):
            self.first_coord = TableCoord.copy (self.last_nonfree_pos)
        else:
            item.private_prev_coord = TableCoord.copy(self.last_coord)
            self.__fetch_w_coord(item.private_prev_coord).private_next_coord = coord_to_put
        self.__get_new_free()
        self.last_coord.replace(coord_to_put)
        item.private_next_coord = None
        self.length += 1


    def __get_new_free(self):
        if (self.last_nonfree_pos.sub_ind == self.cluster_size - 1):
            self.last_nonfree_pos.override(sub_ind=0)
            
            self.last_nonfree_pos.shift_add(super_ind=1)
        else:
            self.last_nonfree_pos.shift_add(sub_ind=1)
    def __resolve_conflict_a(self, x):
        if (self.reclaim_queue[0] == x):
            self.__reclaim_popleft()
    def __resolve_conflict_b(self, x):
        if (self.last_nonfree_pos == x):
            self.__get_new_free()
    def __get_free_coord(self):
        if self.reclaim_queue_len == 0 :
            x = TableCoord.copy(self.last_nonfree_pos)
            self.__resolve_conflict_a(x)
        else:
            x = self.__reclaim_popleft()
            self.__resolve_conflict_b(x)
        return x
    
    def get(self, index) -> CRQPosTracker:
        return self.__fetch_w_coord(self.__index_to_tablecoord(index))
    

    def __index_to_tablecoord(self, index) -> TableCoord: 
        if (index < 0):
            raise IndexError(f"Index out of range.") 
        if (index > self.length - 1):
            raise IndexError(f"Index out of range.")
        cur_coord: TableCoord = self.first_coord
        for i in range(index):
            x = self.__fetch_w_coord(cur_coord) 
            cur_coord = x.private_next_coord
            #print(f"{x=}")
        return cur_coord
    def __calc_table_index(self, table_coord: TableCoord) -> int:
        return table_coord.super_ind * self.cluster_size + table_coord.sub_ind
    def __return_closest_reclaim(self) -> None | tuple[ReclaimCoord, int]:
        if (self.length == 0):
            return None
        out = ReclaimCoord(len(self.__table), self.cluster_size, True)
        min_table_index: int = self.__calc_table_index(TableCoord(len(self.__table) -1, self.cluster_size - 1))
        for i in range(self.reclaim_queue_len):
            
            cur_recl_coord: ReclaimCoord = self.reclaim_queue[i]
            if ((t_index:= self.__calc_table_index(cur_recl_coord)) < min_table_index):
                out = cur_recl_coord
                min_table_index = t_index
                ind = i
        return (out, ind)


    def __reclaim_append(self, table_coord: TableCoord):
        if self.reclaim_queue_len == self.reclaim_slots:
            closest_reclaim = self.__return_closest_reclaim()            
            self.earliest_discard = TableCoord.copy(closest_reclaim[0])
            self.reclaim_queue[closest_reclaim[1]].replace(table_coord)
            self.discarded_reclaim_spot = True
        else:
            x = self.reclaim_queue[self.reclaim_queue_len]
            x.replace(table_coord)
            x.activate()
            self.reclaim_queue_len += 1

    def __check_if_empty_row(self, x: tuple[CRQPosTracker]):
        none_obj = self.none_object_creation_call
        for i in x:
            if (i != none_obj):
                return False
        return True

    @staticmethod
    def __shift_up_by_one_if_equal_or_more(x: TableCoord, threshold: int) -> None:
        if (x.super_ind >= threshold):
            x.shift_add(super_ind=-1)
    def __remove_row(self, super_ind: int):
        self.__table.pop(super_ind)
        for row in self.__table[super_ind:]:
            item: CRQPosTracker
            for item in row:
                for c in (item.private_crq_coord, item.private_next_coord, item.private_prev_coord):
                    self.__shift_up_by_one_if_equal_or_more(c, super_ind)
        gc.collect()

    def remove(self, index):
        if self.is_itering:
            raise ValueError("Cannot remove while iterating.")
        if (index > self.length - 1):
            raise IndexError(f"Index out of range.")
        coord = self.__index_to_tablecoord(index)
        self.__reclaim_append(coord)
        self.length -= 1

        if (index == 0):
            tb_delete = TableCoord.copy(self.first_coord)
            self.first_coord.replace(self.__fetch_w_coord(self.first_coord).private_next_coord)
            self.__place_w_coord(self.none_object_creation_call(), tb_delete)
            self.__fetch_w_coord(self.first_coord).private_prev_coord = None
            return
        if (index == self.length):
            tb_delete = TableCoord.copy(self.last_coord)
            self.last_coord.replace(self.__fetch_w_coord(self.last_coord).private_prev_coord)
            self.__place_w_coord(self.none_object_creation_call(), tb_delete)
            self.__fetch_w_coord(self.last_coord).private_next_coord = None
            
            return
        x: CRQPosTracker = self.__fetch_w_coord(coord)
        prev_coord = x.private_prev_coord
        prev_x: CRQPosTracker = self.__fetch_w_coord(prev_coord)
        next_coord = x.private_next_coord
        next_x: CRQPosTracker = self.__fetch_w_coord(next_coord)
        assert prev_x.private_next_coord == coord
        assert next_x.private_prev_coord == coord
        self.__place_w_coord(self.none_object_creation_call(), coord)
        prev_x.private_next_coord.replace(next_coord)
        next_x.private_prev_coord.replace(prev_coord)
        if self.check_interval_cur >= CRL_CHECK_INTERVAL:
            self.check_interval_cur = 0
            
        
        if self.check_interval_cur >= CRL_CHECK_INTERVAL:
            pass
            # if self.__check_if_empty_row(c:= self.__table[coord.super_ind]):
            #     self.__remove_row(coord.super_ind)
        else:
            self.check_interval_cur += 1
        

        
    def __len__(self):
        return self.length

    def __place_w_coord(self, item, coord: TableCoord) -> CRQPosTracker:
        return self.__place(item, coord.super_ind, coord.sub_ind)
    
    def __fetch_w_coord(self, coord: TableCoord) -> CRQPosTracker:
        return self.__fetch(coord.super_ind, coord.sub_ind)
    

    def __single_reclaim_add_from_find(self):
        if (replaced_with := self.__find_for_reclaim()) is not None:   
            #print(f"{replaced_with=}") 
            self.__reclaim_append(replaced_with)


    def swap(self, a_ind: int , b_ind: int):
        if self.is_itering:
            raise ValueError("Cannot swap while iterating.")
        if (a_ind > self.length - 1 or b_ind > self.length - 1):
            raise IndexError(f"Index out of range.")
        if (a_ind == b_ind):
            return
        
        if (abs(a_ind - b_ind) == 1) and (a_ind > b_ind):
            __a_ind, __b_ind = b_ind, a_ind
        else:
            __a_ind, __b_ind = a_ind, b_ind
        a_coord = TableCoord.copy(self.__index_to_tablecoord(__a_ind))
        
        b_coord = TableCoord.copy(self.__index_to_tablecoord(__b_ind))
        a_item = self.__fetch_w_coord(a_coord)
        b_item = self.__fetch_w_coord(b_coord)
        a_prev_coord = TableCoord.copy(a_item.private_prev_coord) if a_item.private_prev_coord else None
        a_next_coord = TableCoord.copy(a_item.private_next_coord) if a_item.private_next_coord else None
        b_prev_coord = TableCoord.copy(b_item.private_prev_coord) if b_item.private_prev_coord else None
        b_next_coord = TableCoord.copy(b_item.private_next_coord) if b_item.private_next_coord else None
        #TODO: Fix bug when lower = 0
        if (abs(__a_ind - __b_ind) == 1):
            #print("Before:")
            #a_item.crq_print()
            #b_item.crq_print()
            #print("---------------------------")
            if a_item.private_prev_coord:
                self.__fetch_w_coord(a_item.private_prev_coord).private_next_coord = deepcopy(b_coord)

            a_item.private_prev_coord = deepcopy(b_coord)
            if a_item.private_next_coord:
                #print(f"{b_prev_coord=}")
                #print(f"{a_prev_coord=}")
                #print(f"{b_next_coord=}")
                #print(f"{a_next_coord=}")
                a_item.private_next_coord = deepcopy(b_next_coord)
            if b_item.private_prev_coord:
                b_item.private_prev_coord = deepcopy(a_prev_coord)
            if b_item.private_next_coord:
                self.__fetch_w_coord(b_item.private_next_coord).private_prev_coord = deepcopy(a_coord)
            b_item.private_next_coord = deepcopy(a_coord)
            #print("After:")
            #a_item.crq_print()
            #b_item.crq_print()
            #print("")
        else:   
            if a_item.private_prev_coord:
                self.__fetch_w_coord(a_item.private_prev_coord).private_next_coord.replace(b_coord)
            if a_item.private_next_coord:
                self.__fetch_w_coord(a_item.private_next_coord).private_prev_coord.replace(b_coord)
            if b_item.private_prev_coord:
                self.__fetch_w_coord(b_item.private_prev_coord).private_next_coord.replace(a_coord)
            if b_item.private_next_coord:
                self.__fetch_w_coord(b_item.private_next_coord).private_prev_coord.replace(a_coord)
            a_item.private_prev_coord = b_prev_coord
            b_item.private_prev_coord = a_prev_coord
            a_item.private_next_coord = b_next_coord
            b_item.private_next_coord = a_next_coord
        if (__a_ind == 0):
            self.first_coord = b_coord
        if (__b_ind == 0):
            self.first_coord = a_coord    
        if (__a_ind == self.length - 1):
            self.last_coord = b_coord
        if (__b_ind == self.length - 1):
            self.last_coord = a_coord

    def move(self, ind: int, dest: int):
        if self.is_itering:
            raise ValueError("Cannot move while iterating.")
        if (ind > self.length - 1 or dest > self.length - 1):
            raise IndexError(f"Index out of range.")
        if (ind == dest):
            return
        
        if (ind > dest):
            for i in range(ind - dest):
                self.swap(ind-i, ind-i-1)
        if (ind < dest):
            for i in range(dest - ind):
                self.swap(ind+i, ind+i+1)


    def __find_for_reclaim(self) -> None | TableCoord:
        if self.earliest_discard is None:
            return None
        out = TableCoord.copy(self.earliest_discard)
        for i in range(self.earliest_discard.super_ind, len(self.__table)):
            for j in range(self.earliest_discard.sub_ind, self.cluster_size):
                if (i == out.super_ind and j == out.sub_ind):
                    continue
                if self.__table[i][j] == self.none_object_creation_call():
                    if self.earliest_discard:
                        self.earliest_discard.override(i, j)
                    else:
                        self.earliest_discard = TableCoord(i, j)
                    return out
        self.earliest_discard = None
        self.discarded_reclaim_spot = False
        return None

    def __reclaim_popleft(self) -> TableCoord:
        out: TableCoord =  TableCoord.from_reclaim_coord(self.reclaim_queue[0])
        for i in range(self.reclaim_queue_len - 1):
            self.reclaim_queue[i].replace(self.reclaim_queue[i + 1])
        self.reclaim_queue[self.reclaim_queue_len - 1].clear()
        
        self.reclaim_queue_len -= 1
        
        return out
        
    
    def __place(self, item, super_ind, sub_ind):
        if super_ind >= len(self.__table) or sub_ind >= len(self.__table[super_ind]) or super_ind < 0 or sub_ind < 0:
            raise IndexError(f"Index out of range. Super_ind: {super_ind}, sub_ind: {sub_ind}")
        self.__table[super_ind][sub_ind] = item
    
    def __fetch(self, super_ind, sub_ind) -> CRQPosTracker:
        if super_ind >= len(self.__table) or sub_ind >= len(self.__table[super_ind]) or super_ind < 0 or sub_ind < 0:
            raise IndexError(f"Index out of range. Super_ind: {super_ind}, sub_ind: {sub_ind}")
        return self.__table[super_ind][sub_ind] 