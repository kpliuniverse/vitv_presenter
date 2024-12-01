import sys


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
    #print(message_to_write)
    print(f"Arg 1 = {sys.argv[1]}")