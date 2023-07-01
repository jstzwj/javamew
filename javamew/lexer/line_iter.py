
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
    
    def is_eof(self) -> cython.bint:
        return self._iter.is_eof()
    
    def bump(self) -> cython.Py_UCS4:
        c: cython.Py_UCS4 = self._iter.bump()
        if c == "\r":
            if self._iter.first() == "\n":
                self._iter.bump()
                return "\n"
        return c