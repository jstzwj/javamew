
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import unittest

from javamew.lexer.unicode_iter import UnicodeIterator

class TestUnicodeIter(unittest.TestCase):
    def _get_token_list(self, it):
        ret = []
        while not it.is_eof():
            ret.append(it.bump())
        return ret

    def test_escape(self):
        it = UnicodeIterator("\\u0020", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, [" "])
    
    def test_odd_backslash(self):
        it = UnicodeIterator("\\\\u2122", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\\", "\\", "u", "2", "1", "2", "2"])
    
    def test_even_backslash(self):
        it = UnicodeIterator("\\\\\\u2122", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\\", "\\", "™"])
    
    def test_multi_u_escape(self):
        it = UnicodeIterator("abc\\uuuuu0020u", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["a", "b", "c", " ", "u"])

    def test_unicode_backslash(self):
        it = UnicodeIterator("\\u005cu005a", 0)
        tokens = self._get_token_list(it)
        self.assertEqual(tokens, ["\\", "u", "0", "0", "5", "a"])
    
    def test_unicode_invalid_hex(self):
        it = UnicodeIterator("\\u00pC", 0)
        with self.assertRaises(ValueError):
            tokens = self._get_token_list(it)
    
    def test_eof(self):
        it = UnicodeIterator("abc", 0)
        self.assertEqual(it.first(), "a")
        self.assertEqual(it.second(), "b")
        self.assertEqual(it.look_nth(2), "c")
        self.assertEqual(it.look_nth(3), "\0")
        self.assertEqual(it.look_nth(4), "\0")

if __name__ == "__main__":
    unittest.main()
