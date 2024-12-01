import sysv_ipc
from time import sleep

# Create a key (same as in C code)
key = 12

# Create shared memory object (same key as in C code)
memory = sysv_ipc.SharedMemory(key)

# Assuming the C program stores each string as 5 bytes (as per %04d format in C code)
buffer_size = 5  # Size of each string in shared memory
num_entries = 8  # Number of entries in shared memory

# Read values from shared memory
i = 0
while True:
    i += 1
    print(f"======== Loop value: {i} ========")

    # Initialize an empty list to store values
    encoder_values = []

    for j in range(num_entries):
        # Read the corresponding memory chunk
        data = memory.read(buffer_size * (j + 1))[-buffer_size:]  # Read the j-th 5 bytes
        # Convert the bytes to a string (assuming UTF-8 or ASCII encoding)
        try:
            value_str = data.decode('utf-8').strip('\0')  # Remove any null characters from the string
            print(f"Value from shared memory at index {j}: {value_str}")
            encoder_values.append(value_str)
        except UnicodeDecodeError:
            print(f"Error decoding value at index {j}, skipping.")
    
    # Now process the values as integers
    encoder_val = [int(val) for val in encoder_values]
    print(f"Converted integer values: {encoder_val}")

    print("\n")
    sleep(0.1)  # Adjust the sleep as necessary (this is for polling rate)
