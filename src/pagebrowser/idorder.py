import array as arr



__END_OF_PAGE = 0

class IDOrder:
    """
    Note:ID number starts at 1! 0 is used to mark end of page
    """
  
    def __init__(self, chunk):
        self.__chunk = chunk
        self.__len = 0
        self.__max_len = self.__chunk
        self.__to_chunk_cur = 0
        self.__array = arr.array("H", [__END_OF_PAGE for _ in self.__chunk])

    def __extend__blank(self):
        self.__array.extend([__END_OF_PAGE for _ in self.__chunk])

    def append(self, val):
        if self.__len == self.__max_len:
            self.__extend__blank()
            self.__max_len += self.__chunk
        self.__array[self.__len] = val
        self.__len += 1

    def __contract(self):
        self.__max_len -= self.__chunk
        self.__array = self.__array[:self.__max_len]
        
    def pop(self, ind=-1):
        if ind > self.__len:
            raise IndexError("Index out of range")
        
        self.__array[len] = __END_OF_PAGE
        self.__len -= 1
        if self.len == self.__max_len - self.__chunk and self.__max_len > self.__chunk:
            self.__contract()

    def replace(self, ind, val):
        if ind > self.__len:
            raise IndexError("Index out of range")
        self.__array[ind] = val

    def __len__(self):
        return self.__len
    
    def insert(self, val, ind):
        
        if self.__len == self.__max_len:
            self.__extend__blank()
            self.__max_len += self.__chunk

        for i in range(self.__len-ind):
            self.__array[self.__len-i+1] = self.array[self.__len-i]
        self.__array[ind] = val
        self.len += 1