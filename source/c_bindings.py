from ctypes import *


def c_string(string: str, size=None, encoding='utf-8'):
    """
    Convert a Python string to a C string (C char array).

    Args:
        string: Python string object.
        size: (Optional) Size of the string + 1.
        encoding: Encoding of the Python string object.

    Returns:
        c_char_array_size (where 'size' is dependent on the argument passed in).
    """
    return create_string_buffer(bytes(string, encoding), size)


def c_string_array(*strings: str, count=None, encoding='utf-8'):
    """
    Convert a sequence of Python strings to an array of C strings (array of C char array).

    Args:
        *strings: Python string objects.
        count: (Optional) Amount of strings inputted.
        encoding: Encoding of the Python string object.

    Returns:
        LP_c_char_array_size (where 'size' is dependent on the argument passed in).
    """
    if count is None:
        count = len(strings)

    # Create a list of c_char_array and cast them to LP_c_char.
    buffers = [
        cast(
            pointer(c_string(string, encoding=encoding)),
            POINTER(c_char)
        ) for string in strings
    ]

    string_array_type = POINTER(c_char) * count
    string_array = string_array_type()
    string_array[:] = buffers
    return string_array


def c_array(array, c_type, size=None):
    """
    Convert a Python sequence to a C array.

    Args:
        array: Python sequence (that contains int, float, str or bytes)
        c_type: The type to convert to.
        size: (Optional) The size of the array.

    Returns:
        c_type_array_size (where 'c_type' and 'size' are dependent on the arguments passed in).
    """
    if size is None:
        size = len(array)
    buffer_type = c_type * size  # noinspection
    buffer = buffer_type()
    buffer[:] = array
    return buffer


def c_pointer_to_char_pointers(string):
    return cast(pointer(pointer(create_string_buffer(bytes(string, 'utf-8')))), POINTER(POINTER(c_char)))
