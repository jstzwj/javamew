

from typing import Optional

from javamew.diagnostics.engine import Diagnostic
from javamew.lexer.tokenizer import JavaTokenizer
from . import tree

class Parser(object):
    def __init__(self, tokenizer: JavaTokenizer, diagnostic: Optional[Diagnostic] = None) -> None:
        self._tokenizer = tokenizer
        if diagnostic is None:
            diagnostic = Diagnostic()
        self._diagnostic = diagnostic

    def parser(self) -> tree.CompilationUnit:
        return self.parse_compilation_unit()
    
    def parse_compilation_unit(self) -> tree.CompilationUnit:
        pass