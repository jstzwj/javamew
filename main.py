
# message center
from javamew.diagnostics.engine import Diagnostic
diagnostic = Diagnostic()

# char stream
from javamew.lexer.tokenizer import JavaTokenizer
from javamew.lexer.token import TokenKind

with open("tests/source/helloworld.java", "r", encoding="utf-8") as f:
    code = f.read()

from javamew.lexer.unicode_iter import UnicodeIterator
it = UnicodeIterator(code, 0)
while not it.is_eof():
    print(it.bump())

tokenizer = JavaTokenizer(code)

while True:
    token = tokenizer.advance_token()
    print(token.kind)
    if token.is_eof():
        break