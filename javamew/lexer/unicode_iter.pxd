cdef bint is_hex(Py_UCS4 c)
cdef int hex_to_int(Py_UCS4 c)

cdef class UnicodeIterator:
    cdef str _source
    cdef int _len
    cdef int _index
    cdef bint _is_escaped
    cdef int _contiguous_backslashes

    cpdef UnicodeIterator clone(self)
    cdef Py_UCS4 next(self)
    cdef bint _is_eligible(self)
    cdef int advance_by(self, int n)
    cdef Py_UCS4 nth(self, int n)
    cdef Py_UCS4 look_nth(self, int n)
    cdef Py_UCS4 first(self)
    cdef Py_UCS4 second(self)
    cdef eat_while(self, object predicate)
