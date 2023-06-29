
from javamew.basic.char_iter cimport CharIterator
from javamew.diagnostics.engine cimport Diagnostic

cdef class JavaTokenizer:
    cdef CharIterator char_iter
    cdef Diagnostic diagnostic