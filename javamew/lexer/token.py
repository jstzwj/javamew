
import cython

from enum import IntEnum


RESERVED_KEYWORDS = set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case',
                  'catch', 'char', 'class', 'const', 'continue', 'default',
                  'do', 'double', 'else', 'enum', 'extends', 'final',
                  'finally', 'float', 'for', 'goto', 'if', 'implements',
                  'import', 'instanceof', 'int', 'interface', 'long', 'native',
                  'new', 'package', 'private', 'protected', 'public', 'return',
                  'short', 'static', 'strictfp', 'super', 'switch',
                  'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
                  'void', 'volatile', 'while'])

CONTEXTUAL_KEYWORDS = set(['exports', 'module', 'non-sealed', 'open',
                  'opens', 'permits', 'provides', 'record',
                  'requires', 'sealed', 'to', 'transitive',
                  'uses', 'var', 'with', 'yield'])


MODIFIERS = set(['abstract', 'default', 'final', 'native', 'private',
                  'protected', 'public', 'static', 'strictfp', 'synchronized',
                  'transient', 'volatile'])

BASIC_TYPES = set(['boolean', 'byte', 'char', 'double',
                  'float', 'int', 'long', 'short'])

BOOLEAN_TRUE_LITERAL = "true"
BOOLEAN_FALSE_LITERAL = "false"
BOOLEAN_LITERALS = set(['true', 'false'])
NULL_LITERAL = 'null'

SEPARATORS = set(['(', ')', '{', '}', '[', ']', ';', ',', '.'])

OPERATORS = set(['>>>=', '>>=', '<<=',  '%=', '^=', '|=', '&=', '/=',
                '*=', '-=', '+=', '<<', '--', '++', '||', '&&', '!=',
                '>=', '<=', '==', '%', '^', '|', '&', '/', '*', '-',
                '+', ':', '?', '~', '!', '<', '>', '=', '...', '->', '::'])

INFIX_OPERATORS = set(['||', '&&', '|', '^', '&', '==', '!=', '<', '>', '<=', '>=',
                '<<', '>>', '>>>', '+', '-', '*', '/', '%'])

PREFIX_OPERATORS = set(['++', '--', '!', '~', '+', '-'])

POSTFIX_OPERATORS = set(['++', '--'])

ASSIGNMENT_OPERATORS = set(['=', '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=',
                    '<<=', '>>=', '>>>='])

LAMBDA_OPERATORS = set(['->'])

METHOD_REFERENCE_OPERATORS = set(['::',])

ESCAPE_CHARS = set(['b', 's', 't', 'n', 'f', 'r', '\n', '"', '\'', '\\'])

@cython.cclass
class TokenKind:
    UNKNOWN = 0 # Used to traceback
    EOF = 1
    # WhiteSpace
    WhiteSpace = 2
    # Comment = 3, 4
    TraditionalComment = 3
    EndOfLineComment = 4
    # Token = 5, 6, 7, 8
    Identifier = 5
    # Keyword
    ReservedKeyword = 6
    ContextualKeyword = 7
    # Literal
    IntegerLiteral = 8
    FloatingPointLiteral = 9
    BooleanLiteral = 10
    CharacterLiteral = 11
    StringLiteral = 12
    TextBlock = 13
    NullLiteral = 14

    Separator = 8
    Operator = 9

@cython.cclass
class JavaToken:
    def __init__(self, kind: cython.int, value: str, len: cython.int) -> None:
        self._kind: cython.int = kind
        self._value: str = value
        self._len: cython.int = len
    
    def __str__(self) -> str:
        value_str = self._value.replace('\n', '\\n')
        return f"<{self._kind}, {value_str}>"
    
    def __repr__(self) -> str:
        value_str = self._value.replace('\n', '\\n')
        return f"<{self._kind}, \"{value_str}\">"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JavaToken):
            return False
        return self._kind == other.kind and \
            self._value == other.value and \
            self._len == other.len

    @property
    def kind(self) -> cython.int:
        return self._kind
    
    @property
    def value(self) -> str:
        return self._value

    @property
    def len(self) -> int:
        return self._len
    
    def is_eof(self) -> bool:
        return self._kind == TokenKind.EOF