
cdef class CharIterator:
    cdef str _source
    cdef int _len
    cdef int _index
    cdef Py_UCS4 next(self)
    cpdef Py_UCS4 bump(self)
    cdef int advance_by(self, int n)
    cdef Py_UCS4 nth(self, int n)
    cdef Py_UCS4 look_nth(self, int n)
    cdef Py_UCS4 first(self)
    cdef Py_UCS4 second(self)
    cdef eat_while(self, object predicate)
