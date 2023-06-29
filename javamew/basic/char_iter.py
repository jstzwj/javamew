
import cython

@cython.cclass
class CharIterator:
    def __init__(self, source: str, index: cython.int) -> None:
        self._source: str = source
        self._len: cython.int = len(source)
        self._index: cython.int = index

    @cython.boundscheck(False)
    def next(self) -> cython.Py_UCS4:
        c = cython.declare(cython.Py_UCS4)
        if self._index < self._len:
            c = self._source[self._index]
            self._index += 1
            return c
        else:
            return '\0'

    def advance_by(self, n: cython.int) -> cython.int:
        for i in range(n):
            if self.next() == '\0':
                return i
        return n

    def nth(self, n: cython.int) -> cython.Py_UCS4:
        self.advance_by(n)
        return self.next()
    
    @cython.boundscheck(False)
    def look_nth(self, n: cython.int) -> cython.Py_UCS4:
        if self._index + n >= self._len:
            return '\0'
        else:
            return self._source[self._index + n]

    @cython.boundscheck(False)
    def as_str(self) -> str:
        return self._source[self._index:]
