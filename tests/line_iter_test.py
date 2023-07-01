
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import unittest

from javamew.lexer.unicode_iter import UnicodeIterator
from javamew.lexer.line_iter import LineIterator

class TestLineIter(unittest.TestCase):
    def _get_token_list(self, it):
        ret = []
        while not it.is_eof():
            ret.append(it.bump())
        return ret

    def test_escape(self):
        it = LineIterator(UnicodeIterator("\\u0020", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, [" "])

        it = LineIterator(UnicodeIterator("\\u000D\\u000A", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n"])

        it = LineIterator(UnicodeIterator("\\u000D", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\r"])

        it = LineIterator(UnicodeIterator("\\u000A", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n"])
    
    
    def test_lf(self):
        it = LineIterator(UnicodeIterator("\n", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n"])

        it = UnicodeIterator("\n\n", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n", "\n"])
    
    def test_cr(self):
        it = LineIterator(UnicodeIterator("\r", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\r"])

        it = LineIterator(UnicodeIterator("\r\r", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\r", "\r"])
    
    def test_crlf(self):
        it = LineIterator(UnicodeIterator("\r\n", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n"])

        it = LineIterator(UnicodeIterator("\r\n\r\n \r \n", 0))
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\n", "\n", " ", "\r", " ", "\n"])
    
if __name__ == "__main__":
    unittest.main()
