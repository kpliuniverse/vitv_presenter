import sysv_ipc
from time import sleep

# Create a key
key = 12

# Create shared memory object
memory = sysv_ipc.SharedMemory(key)

i = 0
# Read value from shared memory
while True:
    memory_value = memory.read().decode('utf-8')
    print(memory_value)

    # Putting those values in a list
    encoder_str = memory_value.split('\0')
    encoder_str = list(filter(None, encoder_str))

    # Convert str into list of integers
    encoder_val = list(map(int, encoder_str))
    print(encoder_val)
    i += 1
    print("\n Loop value i is: ")
    print(i)
    print("\n")
    # sleep(0.0001)