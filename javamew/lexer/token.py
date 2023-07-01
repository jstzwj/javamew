
import cython

from enum import IntEnum

@cython.cclass
class TokenKind:
    EOF = 1
    # WhiteSpace
    WhiteSpace = 2
    # Comment = 3, 4
    TraditionalComment = 3
    EndOfLineComment = 4
    # Token = 5, 6, 7, 8
    Identifier = 5
    Keyword = 6
    Literal = 7
    Separator = 8
    Operator = 9

@cython.cclass
class JavaToken:
    def __init__(self, kind: cython.int, value: str, len: cython.int) -> None:
        self._kind: cython.int = kind
        self._value: str = value
        self._len: cython.int = len
    
    def __str__(self) -> str:
        return f"<{self._kind}, {self._value}>"
    
    def __repr__(self) -> str:
        return f"<{self._kind}, \"{self._value}\">"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JavaToken):
            return False
        return self._kind == other.kind and \
            self._value == other.value and \
            self._len == other.len

    @property
    def kind(self) -> cython.int:
        return self._kind
    
    @property
    def value(self) -> str:
        return self._value

    @property
    def len(self) -> int:
        return self._len
    
    def is_eof(self) -> bool:
        return self._kind == TokenKind.EOF