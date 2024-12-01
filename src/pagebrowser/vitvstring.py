
from typing import Callable
import numpy as np
from numpy.typing import NDArray


np.seterr(over='raise')

def create_consistent_size_int_tuple_from_string_callable(limit: int) -> Callable[[int], NDArray[np.int32]]:
    if ((limit - 1) & limit) != 0:
        return ValueError ("Powers of two only")
    
    return lambda x: __create_consistent_size_string_tuple(x, limit)



def __create_consistent_size_string_tuple(string: str, limit: int) -> NDArray[np.int32]:
    namelen: int = len(string)
    if (namelen > limit):
        raise ValueError("String too long")
    fin_str: str = string + "\0" * (limit - namelen)
    assert len(fin_str) == limit
    arr = np.array([ord(c) for c in fin_str], dtype=np.int32)
    arr.flags.writeable = False
    return arr