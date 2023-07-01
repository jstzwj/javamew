
from javamew.lexer.unicode_iter cimport UnicodeIterator
from javamew.lexer.line_iter cimport LineIterator
from javamew.diagnostics.engine cimport Diagnostic
from javamew.lexer.token cimport JavaToken

cdef class JavaTokenizer:
    cdef UnicodeIterator _char_iter
    cdef LineIterator _iter
    cdef Diagnostic _diagnostic

    cpdef JavaToken advance_token(self)