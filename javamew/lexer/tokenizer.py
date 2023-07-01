
from typing import Optional
import cython
from javamew.diagnostics.engine import Diagnostic

from .unicode_iter import UnicodeIterator
from .line_iter import LineIterator
from .token import JavaToken, TokenKind

def is_line_terminator(c: cython.Py_UCS4) -> cython.bint:
    if c == 0x000A or c == 0x000D:
        '''
        the ASCII LF character, also known as "newline"
        the ASCII CR character, also known as "return"
        the ASCII CR character followed by the ASCII LF character
        '''
        return True
    else:
        return False


def is_whitespace(c: cython.Py_UCS4) -> cython.bint:
    c: cython.int = ord(c)
    if c == 0x0020 or c == 0x0009 or c == 0x000b or c == 0x000c:
        '''
        the ASCII SP character, also known as "space" 0x0020
        the ASCII HT character, also known as "horizontal tab" 0x0009
        the ASCII FF character, also known as "form feed" 0x0x0c
        and vertical tab 0x000b
        '''
        return True
    elif is_line_terminator(c):
        # The character is a whitespace character newline
        return True
    elif c >= 0x2000 and c <= 0x200a:
        # The character is a whitespace character in the Unicode category "Space Separator"
        return True
    elif c == 0x202f or c == 0x205f or c == 0x3000:
        # The character is a whitespace character in the Unicode category "Other Separator"
        return True
    else:
        # The character is not a whitespace character
        return False

def is_comment_start(first_char: cython.Py_UCS4, second_char: cython.Py_UCS4) -> cython.bint:
    return (first_char == "/" and second_char == "*") or \
                (first_char == "/" and second_char == "/")

@cython.cclass
class JavaTokenizer:
    def __init__(self, source: str, diagnostic: Optional[Diagnostic] = None) -> None:
        self._char_iter = UnicodeIterator(source, 0)
        self._iter = LineIterator(self._char_iter)
        if diagnostic is None:
            diagnostic = Diagnostic()
        self._diagnostic = diagnostic
    
    def is_eof(self) -> cython.bint:
        return self._iter.is_eof()

    def advance_token(self) -> JavaToken:
        it = self._iter.clone()

        start_pos = self._iter.index()
        first_char = self._iter.first()
        second_char = self._iter.second()
        token_kind: cython.int = TokenKind.EOF

        if is_whitespace(first_char):
            # whitespace
            token_kind = self.whitespace()
        elif is_comment_start(first_char, second_char):
            # comment
            token_kind = self.comment()
        elif first_char == "\\":
            pass
        else:
            pass
        
        end_pos = self._iter.index()
        token_len = end_pos - start_pos
        token_text = ""
        while it.index() < self._iter.index():
            token_text += it.bump()
        return JavaToken(token_kind, token_text, token_len)
    
    def whitespace(self) -> cython.int:
        self._iter.bump()
        return TokenKind.WhiteSpace
    
    def comment(self) -> cython.int:
        self._iter.bump() # bump slash
        second_char = self._iter.first()
        if second_char == "*":
            return self._traditional_comment()
        elif second_char == "/":
            return self._endofline_comment()
        else:
            raise ValueError("Lexer: Tokenize Comments Error.")
    
    def _traditional_comment(self) -> cython.int:
        self._iter.bump() # bump star
        while not self._iter.is_eof():
            current_char = self._iter.bump()
            if current_char == "*" and self._iter.first() == "/":
                self._iter.bump() # bump slash
                return TokenKind.TraditionalComment

        raise ValueError("Lexer: Unclosed comment.")

    def _endofline_comment(self) -> cython.int:
        while not self._iter.is_eof():
            current_char = self._iter.bump()
            if is_line_terminator(current_char):
                return TokenKind.EndOfLineComment

        return TokenKind.EndOfLineComment