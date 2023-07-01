
from .unicode_iter cimport UnicodeIterator

cdef class LineIterator:
    cdef UnicodeIterator _iter

    cpdef bint is_eof(self)
    cdef Py_UCS4 look_nth(self, int n)
    cdef Py_UCS4 first(self)
    cdef Py_UCS4 second(self)
    cdef eat_while(self, object predicate)