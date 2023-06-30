
from javamew.lexer.unicode_iter cimport UnicodeIterator
from javamew.diagnostics.engine cimport Diagnostic

cdef class JavaTokenizer:
    cdef UnicodeIterator unicode_iter
    cdef Diagnostic diagnostic