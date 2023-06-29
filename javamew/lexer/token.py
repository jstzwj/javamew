
import cython

from enum import IntEnum

@cython.cclass
class TokenKind:
    EOF = 1
    WhiteSpace = 2
    Comment = 3

@cython.cclass
class JavaToken:
    def __init__(self, kind: cython.int, value: str, len: cython.int) -> None:
        self._kind: cython.int = kind
        self._value: str = value
        self._len: cython.int = len
    
    @property
    def kind(self) -> int:
        return self._kind

    @property
    def len(self) -> int:
        return self._len
    
    def is_eof(self) -> bool:
        return self._kind == TokenKind.EOF