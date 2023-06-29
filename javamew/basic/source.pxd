

cdef class SourceFile:
    cdef str path

cdef class Position:
    cdef int line
    cdef int column

cdef class SourcePosition:
    cdef SourceFile source
    cdef Position position

cdef class Range:
    cdef Position start_pos
    cdef Position end_pos

cdef class SourceRange:
    cdef SourceFile source
    cdef Range range
