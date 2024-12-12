import sys
import mmap
import time


def string_to_ascii_tuple(input_string):
    # Check for non-ASCII characters
    for char in input_string:
        if ord(char) > 127:  # ASCII range is 0-127
            raise ValueError(f"Non-ASCII character detected: {char}")
    
    # Convert the string to a tuple of ASCII values
    ascii_tuple = tuple(ord(char) for char in input_string)
    
    return ascii_tuple

if __name__ == "__main__": 
    message_to_write = string_to_ascii_tuple("Hello from python\0")
    message_to_write_2 = string_to_ascii_tuple("Now thats IPC!\0")
    #print(message_to_write)
    mmap_name = sys.argv[1]
    print(f"Arg 1 = {mmap_name}")
    with open(mmap_name, mode="r+b") as shmem_file:
        with mmap.mmap(shmem_file.fileno(), length = 64, access=mmap.ACCESS_WRITE) as shmem:
            time.sleep(4)
            for i, b in enumerate(message_to_write):
                shmem[i+1] = b
            shmem[0] = 1
            time.sleep(5)
            while (True):
                if (shmem[0] == 0):
                    break
                time.sleep(2)
            for i, b in enumerate(message_to_write_2):
                shmem[i+1] = b 
            shmem[0] = 1
            time.sleep(5)