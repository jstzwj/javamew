
cdef class UnicodeIterator:
    cdef str _source
    cdef int _len
    cdef int _index
    cdef bint _is_escaped
    cdef int _contiguous_backslashes

    cpdef UnicodeIterator clone(self)
    cdef Py_UCS4 next(self)

    cpdef bint is_eof(self)
    cdef bint _is_eligible(self)
    cdef int advance_by(self, int n)
    cdef Py_UCS4 nth(self, int n)
    cpdef Py_UCS4 look_nth(self, int n)
    cpdef Py_UCS4 first(self)
    cpdef Py_UCS4 second(self)
    cdef eat_while(self, object predicate)
