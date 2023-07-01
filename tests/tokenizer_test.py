
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
    
if __name__ == "__main__":
    unittest.main()
