
from typing import Callable
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

@cython.cclass
class UnicodeIterator:
    """
    REF: https://docs.oracle.com/javase/specs/jls/se20/html/jls-3.html#jls-3.3
    """
    def __init__(self, source: str, index: cython.int) -> None:
        self._source: str = source
        self._len: cython.int = len(source)
        self._index: cython.int = index
        self._is_escaped: cython.bint = False
        self._contiguous_backslashes: cython.int = 0
    
    def clone(self) -> "UnicodeIterator":
        it = UnicodeIterator(
            self._source,
            self._index,
        )
        it._is_escaped = self._is_escaped
        it._contiguous_backslashes = self._contiguous_backslashes
        return it

    @cython.boundscheck(False)
    def next(self) -> cython.Py_UCS4:
        c = cython.declare(cython.Py_UCS4)
        if self._index < self._len:
            c = self._source[self._index]
            self._index += 1
            return c
        else:
            return '\0'
    
    def _is_eligible(self) -> cython.bint:
        if self._is_escaped:
            return True
        elif self._contiguous_backslashes % 2 == 1:
            return True
        return False
    
    def bump(self) -> cython.Py_UCS4:
        c: cython.Py_UCS4 = self.next()
        if c == '\\':
            self._contiguous_backslashes += 1
            # if backslash eligible
            if self._is_eligible():
                # escape unicode chars
                if self.first() == "u":
                    self.next()
                    while self.first() == "u":
                        self.next()

                    value = 0
                    hex_char = []
                    i: cython.int = 0
                    while i < 4:
                        c = self.next()
                        hex_char.append(c)
                        if is_hex(c):
                            value += 16**(3-i) * hex_to_int(c)
                        else:
                            raise ValueError(f"Illegal escape character {''.join(hex_char)}.")
                        i += 1
                    self._is_escaped = True
                    return chr(value)
        else:
            self._contiguous_backslashes = 0
        self._is_escaped = False
        return c
                
    def advance_by(self, n: cython.int) -> cython.int:
        for i in range(n):
            if self.bump() == '\0':
                return i
        return n

    def nth(self, n: cython.int) -> cython.Py_UCS4:
        self.advance_by(n)
        return self.bump()
    
    def is_eof(self) -> cython.bint:
        return self._index == self._len
    
    @cython.boundscheck(False)
    def look_nth(self, n: cython.int) -> cython.Py_UCS4:
        it = self.clone()
        c: cython.Py_UCS4 = "\0"
        while not it.is_eof() and n >= 0:
            c = it.bump()
            n -= 1
        return c

    def first(self) -> cython.Py_UCS4:
        return self.look_nth(0)

    def second(self) -> cython.Py_UCS4:
        return self.look_nth(1)
    
    def eat_while(self, predicate: Callable[[cython.Py_UCS4], bool]):
        while predicate(self.first()) and not self.is_eof():
            self.bump()

    @cython.boundscheck(False)
    def as_str(self) -> str:
        return self._source[self._index:]
