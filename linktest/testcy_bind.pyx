cdef extern from "test.c":
    void greetings()
    int add (int x, int y)

cpdef cy_greet():
    greetings()

cpdef cy_add(x, y):
    return add (x, y)