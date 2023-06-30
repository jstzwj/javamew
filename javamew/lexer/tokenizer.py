
from typing import Optional
import cython
from javamew.diagnostics.engine import Diagnostic

from .unicode_iter import UnicodeIterator
from .token import JavaToken, TokenKind

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
    elif c >= 0x2000 and c <= 0x200a:
        # The character is a whitespace character in the Unicode category "Space Separator"
        return True
    elif c == 0x202f or c == 0x205f or c == 0x3000:
        # The character is a whitespace character in the Unicode category "Other Separator"
        return True
    else:
        # The character is not a whitespace character
        return False

def is_lineterminator(c: cython.Py_UCS4) -> cython.bint:
    if c == 0x000A or c == 0x000D:
        '''
        the ASCII LF character, also known as "newline"
        the ASCII CR character, also known as "return"
        the ASCII CR character followed by the ASCII LF character
        '''
        return True
    else:
        return False


@cython.cclass
class JavaTokenizer:
    def __init__(self, source: str, diagnostic: Optional[Diagnostic] = None) -> None:
        self.unicode_iter = UnicodeIterator(source, 0)
        if diagnostic is None:
            diagnostic = Diagnostic()
        self.diagnostic = diagnostic

    def advance_token(self) -> JavaToken:
        it = self.unicode_iter.clone()

        start_pos = self.unicode_iter._index
        c = self.unicode_iter.first()
        token_kind: cython.int = TokenKind.EOF
        if is_whitespace(c):
            token_kind = self.whitespace()
        elif c == "\\":
            pass
        elif c == "/":
            pass
        else:
            pass
        
        end_pos = self.unicode_iter._index
        token_len = end_pos - start_pos
        token_text = ""
        while it._index < self.unicode_iter._index:
            token_text += it.bump()
        return JavaToken(token_kind, token_text, token_len)
    
    def whitespace(self) -> cython.int:
        self.eat_while(is_whitespace)
        return TokenKind.WhiteSpace