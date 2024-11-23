import cffi


SOURCES = ('test.c')

ffi = cffi.FFI()
ffi.cdef("""\
int add(int x, int y); 
    """)
ffi.set_source(
    'testcffi',
    """
    #include "test.h"
    """,
    sources = ["test.c"],
)


if __name__ == "__main__":
    ffi.compile()