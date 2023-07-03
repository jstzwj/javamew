

from javamew.lexer.tokenizer import JavaTokenizer
from javamew.parser.ast import Node
from javamew.parser.tree import CompilationUnit


node = Node()
print(node.attrs)

unit = CompilationUnit()
print(unit)