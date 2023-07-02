
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import unittest

from javamew.lexer.tokenizer import JavaTokenizer
from javamew.lexer.token import JavaToken, TokenKind

class TestUnicodeIter(unittest.TestCase):
    def _get_tokens(self, it):
        ret = []
        while not it.is_eof():
            ret.append(it.advance_token())
        return ret

    def test_spaces(self):
        tokenizer = JavaTokenizer("   ")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [JavaToken(TokenKind.WhiteSpace, " ", 1)] * 3)
    
    def test_comments(self):
        tokenizer = JavaTokenizer(" //abc")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.EndOfLineComment, "//abc", 5),
        ])

        tokenizer = JavaTokenizer(" /*abc**/ ")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.TraditionalComment, "/*abc**/", 8),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
        ])

        with self.assertRaises(ValueError):
            tokenizer = JavaTokenizer(" /*abc**")
            tokens = self._get_tokens(tokenizer)
    
    def test_identifiers(self):
        tokenizer = JavaTokenizer("MAX_VALUE")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.Identifier, "MAX_VALUE", 9),
        ])
        
        tokenizer = JavaTokenizer("αρετη αρετ")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.Identifier, "αρετη", 5),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.Identifier, "αρετ", 4),
        ])
    
    def test_keywords(self):
        tokenizer = JavaTokenizer("public static class Big_ma// Nice!")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.ReservedKeyword, "public", 6),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.ReservedKeyword, "static", 6),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.ReservedKeyword, "class", 5),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.Identifier, "Big_ma", 6),
            JavaToken(TokenKind.EndOfLineComment, "// Nice!", 8),
        ])
    
    def test_characters(self):
        tokenizer = JavaTokenizer("'a''b'")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.CharacterLiteral, "'a'", 3),
            JavaToken(TokenKind.CharacterLiteral, "'b'", 3),
        ])
        tokenizer = JavaTokenizer("'\\023' 'b'")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.CharacterLiteral, "'\\023'", 6),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
            JavaToken(TokenKind.CharacterLiteral, "'b'", 3),
        ])
    
    def test_strings(self):
        tokenizer = JavaTokenizer("\"abcd\" ")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.StringLiteral, "\"abcd\"", 6),
            JavaToken(TokenKind.WhiteSpace, " ", 1),
        ])
        tokenizer = JavaTokenizer("\"abcd\"\n")
        tokens = self._get_tokens(tokenizer)
        self.assertEqual(tokens, [
            JavaToken(TokenKind.StringLiteral, "\"abcd\"", 6),
            JavaToken(TokenKind.WhiteSpace, "\n", 1),
        ])

        with self.assertRaises(ValueError):
            tokenizer = JavaTokenizer("\"abcd\r\n\"\n")
            tokens = self._get_tokens(tokenizer)
    
if __name__ == "__main__":
    unittest.main()
