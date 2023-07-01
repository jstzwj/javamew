
from .unicode_iter cimport UnicodeIterator

cdef class LineIterator:
    cdef UnicodeIterator _iter

    cpdef bint is_eof(self)