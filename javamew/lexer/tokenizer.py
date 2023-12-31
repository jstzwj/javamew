
from typing import Optional
import cython
from javamew.basic.character import is_java_identifier_part, is_java_identifier_start
from javamew.diagnostics.engine import Diagnostic
from javamew.lexer.char_utils import is_digit, is_hex, is_octal, is_zero_to_three

from .unicode_iter import UnicodeIterator
from .line_iter import LineIterator
from .token import BOOLEAN_FALSE_LITERAL, BOOLEAN_LITERALS, BOOLEAN_TRUE_LITERAL, CONTEXTUAL_KEYWORDS, ESCAPE_CHARS, NULL_LITERAL, OPERATOR_CHARS, OPERATORS, RESERVED_KEYWORDS, SEPARATORS, JavaToken, TokenKind


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

        if is_whitespace(first_char) or is_line_terminator(first_char):
            # whitespace
            token_kind = self.whitespace()
        elif is_comment_start(first_char, second_char):
            # comment
            token_kind = self.comment()
        else:
            token_kind = self.token()
        
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
    
    def token(self) -> cython.int:
        c = self._iter.first()
        if is_java_identifier_start(c):
            token_text = self._get_identifier_chars()
            # Boolean Literals
            if token_text == BOOLEAN_TRUE_LITERAL or token_text == BOOLEAN_FALSE_LITERAL:
                return TokenKind.BooleanLiteral
            # Null Literals
            if token_text == NULL_LITERAL:
                return TokenKind.NullLiteral
            # Keywords and identifiers
            return self._keywords(token_text)
        elif c == "\"":
            second_char = self._iter.look_nth(1)
            third_char = self._iter.look_nth(2)
            if second_char == "\"" and third_char == "\"":
                # TextBlock
                return self._text_block()
            else:
                # StringLiteral
                return self._string_literal()
        elif c == "\'":
            # CharacterLiteral
            return self._character_literal()
        elif is_digit(c) or c == "." or c == "-":
            # IntegerLiteral and FloatingPointLiteral
            token_kind = self._integer_and_floating_point_literal()
        elif c in SEPARATORS:
            return self._separator()
        else:
            token_kind = self._operator()
            if token_kind != TokenKind.UNKNOWN:
                return token_kind
            else:
                raise ValueError("Could not process token")
    
    def _get_identifier_chars(self) -> str:
        token_text = ""
        token_text += self._iter.bump()
        while is_java_identifier_part(self._iter.first()):
            token_text += self._iter.bump()
        return token_text
    
    def _identifiers(self, token_text: str) -> cython.int:
        if token_text not in RESERVED_KEYWORDS and \
            token_text not in BOOLEAN_LITERALS and \
            token_text != NULL_LITERAL:
            return TokenKind.Identifier

    def _keywords(self, token_text: str) -> cython.int:
        if token_text in RESERVED_KEYWORDS:
            return TokenKind.ReservedKeyword
        elif token_text in CONTEXTUAL_KEYWORDS:
            return TokenKind.ContextualKeyword
        else:
            return TokenKind.Identifier
    
    def _escape_sequences(self) -> cython.int:
        c = self._iter.first()
        if c in ESCAPE_CHARS:
            self._iter.bump()
        elif is_zero_to_three(c):
            self._iter.bump()
            if is_octal(c): self._iter.bump()
            if is_octal(c): self._iter.bump()
        elif is_octal(c):
            self._iter.bump()
            if is_octal(c): self._iter.bump()

    def _character_literal(self) -> cython.int:
        open_c = self._iter.bump()
        c = self._iter.bump()
        if c == "'":
            raise ValueError("Empty character literal")
        elif c == "\n":
            raise ValueError("Unclosed character literal")
        elif c == "\\":
            self._escape_sequences()
        close_c = self._iter.bump()
        if close_c != "'":
            raise ValueError("Too many characters in character literal")
        return TokenKind.CharacterLiteral

    def _text_block(self) -> cython.int:
        self._iter.bump() # bump quote
        self._iter.bump() # bump quote
        self._iter.bump() # bump quote

        self._iter.eat_while(is_whitespace)

        newline = self._iter.bump()
        if not is_line_terminator(newline):
            raise ValueError("Illegal text block start: missing new line after opening quotes")
        
        while not self._iter.is_eof():
            current_char = self._iter.first()
            if current_char == "\\":
                self._escape_sequences()
            elif current_char == "\"":
                second_char = self._iter.look_nth(1)
                third_char = self._iter.look_nth(2)
                if second_char == "\"" and third_char == "\"":
                    break
                self._iter.bump()
            else:
                self._iter.bump()
        
        c = self._iter.bump() # bump quote
        if c != "\"":
            raise ValueError("Unclosed text block")
        c = self._iter.bump() # bump quote
        if c != "\"":
            raise ValueError("Unclosed text block")
        c = self._iter.bump() # bump quote
        if c != "\"":
            raise ValueError("Unclosed text block")
        return TokenKind.TextBlock

    def _string_literal(self) -> cython.int:
        self._iter.bump() # bump quote

        while not self._iter.is_eof():
            current_char = self._iter.first()
            if current_char == "\\":
                self._escape_sequences()
            elif current_char == "\"":
                break
            elif is_line_terminator(current_char):
                raise ValueError("Illegal line end in string literal")
            else:
                self._iter.bump()
        c = self._iter.bump() # bump quote
        if c != "\"":
            raise ValueError("Unclosed string literal")
        return TokenKind.StringLiteral
    
    def _integer_and_floating_point_literal(self) -> cython.int:
        c = self._iter.first()
        c_next = self._iter.second()
        if c == '0' and c_next in 'xX':
            token_kind = self._hex_integer_literal()
            if token_kind == TokenKind.UNKNOWN:
                token_kind = self._hex_floating_point_literal()
            return token_kind
        elif c == '0' and c_next in 'bB':
            return self._binary_integer_literal()
        elif c == '0' and c_next in '01234567':
            self._octal_integer_literal()
        else:
            return self._decimal_literal()

    def _decimal_literal(self) -> cython.int:
        it = self._iter.clone()
        c = it.first()
        if c == "0":
            it.bump()
        elif is_digit(c):
            it.bump()
        else:
            return TokenKind.UNKNOWN

    def _hex_integer_literal(self) -> cython.int:
        it = self._iter.clone()
        it.bump() # bump zero
        it.bump() # bump x

        c = it.bump()
        if not is_hex(c):
            raise ValueError("Hexadecimal numbers must contain at least one hexadecimal digit")
        
        while not it.is_eof():
            current_char = it.first()
            if is_hex(current_char):
                it.bump()
            elif current_char == "_":
                next_char = it.second()
                if is_hex(next_char) or next_char == "_":
                    it.bump()
                else:
                    raise ValueError("Illegal underscore")
            elif current_char == "." or current_char in "pP":
                return TokenKind.UNKNOWN
            else:
                break
        self._iter = it
        return TokenKind.HexIntegerLiteral

    def _hex_floating_point_literal(self) -> cython.int:
        it = self._iter.clone()
        it.bump() # bump zero
        it.bump() # bump x

    def _octal_integer_literal(self) -> cython.int:
        self._iter.bump() # bump zero
        self._iter.bump() # bump 0-7
        

    def _binary_integer_literal(self) -> cython.int:
        self._iter.bump() # bump zero
        self._iter.bump() # bump b
        
    def _integer_type_suffix(self, it) -> None:
        c = it.first()
        if c == "l" or c == "L":
            it.bump()
        return
    
    def _separator(self) -> cython.int:
        c = self._iter.first()
        if c in SEPARATORS:
            self._iter.bump()
            return TokenKind.Separator
        else:
            return TokenKind.UNKNOWN
    
    def _operator(self) -> cython.int:
        it = self._iter.clone()
        operator_str = ""
        for l in range(4):
            c = it.bump()
            operator_str += c
            if c not in OPERATOR_CHARS:
                break
            if operator_str in OPERATORS:
                self._iter = it
                return TokenKind.Operator
        return TokenKind.UNKNOWN


