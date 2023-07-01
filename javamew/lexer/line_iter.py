
from typing import Callable
import cython

from .unicode_iter import UnicodeIterator

@cython.cclass
class LineIterator:
    """
    REF: https://docs.oracle.com/javase/specs/jls/se20/html/jls-3.html#jls-LineTerminator
    LineTerminator:
        the ASCII LF character, also known as "newline"
        the ASCII CR character, also known as "return"
        the ASCII CR character followed by the ASCII LF character
    """
    def __init__(self, it: UnicodeIterator) -> None:
        self._iter: UnicodeIterator = it
    
    def clone(self) -> "LineIterator":
        new_iter = self._iter.clone()
        return LineIterator(new_iter)
    
    def index(self) -> cython.int:
        return self._iter._index
    
    def is_eof(self) -> cython.bint:
        return self._iter.is_eof()
    
    def bump(self) -> cython.Py_UCS4:
        c: cython.Py_UCS4 = self._iter.bump()
        if c == "\r":
            if self._iter.first() == "\n":
                self._iter.bump()
                return "\n"
        return c
    
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
    
    def eat_while(self, predicate: Callable[[cython.Py_UCS4], bool]) -> None:
        while predicate(self.first()) and not self.is_eof():
            self.bump()