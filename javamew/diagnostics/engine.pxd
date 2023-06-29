from javamew.basic.source cimport SourcePosition


cdef class DiagnosticMessage:
    cdef int _severity
    cdef str _message
    cdef SourcePosition _location

cdef class Diagnostic:
    cdef list messages
    cpdef add(self, DiagnosticMessage diagnostic_message)
    cpdef error(self, str message, SourcePosition location)
    cpdef clear(self)