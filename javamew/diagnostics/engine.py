
from ..basic.source import SourcePosition
from enum import IntEnum
import cython

@cython.cclass
class Severity:
    Ignored = 1
    Note = 2
    Warning = 3
    Error = 4
    Fatal = 5

@cython.cclass
class DiagnosticMessage:
    def __init__(self, severity: cython.int, message: str, location: SourcePosition) -> None:
        self._severity: cython.int = severity
        self._message: str = message
        self._location: SourcePosition = location

    @property
    def message(self) -> str:
        return self._message

    @property
    def location(self) -> SourcePosition:
        return self._location

@cython.cclass
class Diagnostic:
    def __init__(self) -> None:
        self.messages = []

    @cython.ccall
    def add(self, diagnostic_message: DiagnosticMessage):
        self.messages.append(diagnostic_message)
    
    @cython.ccall
    def error(self, message: str, location: SourcePosition):
        self.add(DiagnosticMessage(4, message, location))

    @cython.ccall
    def clear(self):
        self.messages.clear()

    def __len__(self) -> int:
        return len(self.messages)

    def __repr__(self) -> str:
        ret = ""
        for i, msg in enumerate(self.messages):
            ret += msg.message
            ret += '\n'
            ret += msg.location.source
            ret += '\n'
            before_spaces = msg.location.offset - 1
            ret += ' ' * before_spaces + '^'

            if i != len(self.messages) - 1:
                ret += '\n'
        return ret