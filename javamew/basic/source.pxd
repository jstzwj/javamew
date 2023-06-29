
cdef class Position:
    cdef int line
    cdef int column

cdef class SourceRange:
    cdef Position start_pos
    cdef Position end_pos
