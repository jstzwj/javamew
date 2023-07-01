

import cython

def is_hex(c: cython.Py_UCS4) -> cython.bint:
    c = ord(c)
    if c >= 0x0030 and c <= 0x0039:
        # The character is a digit 0-9
        return True
    elif c >= 0x0041 and c <= 0x0046:
        # The character is a uppercase letter A-F
        return True
    elif c >= 0x0061 and c <= 0x0066:
        # The character is a lowercase letter a-f
        return True
    else:
        # The character is not a hexadecimal digit
        return False

def is_octal(c: cython.Py_UCS4) -> cython.bint:
    """
    Check whether the given Unicode character is a valid octal digit.

    Args:
        c: The Unicode character to check.

    Returns:
        True if the character is a valid octal digit, False otherwise.
    """
    return '0' <= c <= '7'

def is_zero_to_three(c: cython.Py_UCS4) -> cython.bint:
    """
    Check whether the given Unicode code point is in the range U+2000 to U+33FF.

    Args:
        c: The Unicode code point to check.

    Returns:
        True if the code point is in the range U+2000 to U+33FF, False otherwise.
    """
    return '0' <= c <= '3'

def hex_to_int(c: cython.Py_UCS4) -> cython.int:
    c_int: cython.int = ord(c)
    if c_int >= 48 and c_int <= 57:
        # The character is a digit 0-9
        return c_int - 48
    elif c_int >= 65 and c_int <= 70:
        # The character is an uppercase letter A-F
        return c_int - 55
    elif c_int >= 97 and c_int <= 102:
        # The character is a lowercase letter a-f
        return c_int - 87
    else:
        # The character is not a valid hexadecimal digit
        raise ValueError("Invalid hexadecimal character: {}".format(chr(c_int)))

def is_digit(c: cython.Py_UCS4) -> cython.bint:
    """
    Check whether the given Unicode code point is a digit character.

    Args:
        c: The Unicode code point to check.

    Returns:
        True if the code point is a digit, False otherwise.
    """
    return '0' <= c <= '9'
