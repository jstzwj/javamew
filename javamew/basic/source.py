

import cython

@cython.cclass
class SourceFile:
    def __init__(self, path: str) -> None:
        self.path = path


@cython.cclass
class Position:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

@cython.cclass
class SourcePosition:
    def __init__(self, source: SourceFile, position: Position) -> None:
        self.source = source
        self.position = position


@cython.cclass
class Range:
    def __init__(self, start_pos: Position, end_pos: Position) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos

@cython.cclass
class SourceRange:
    def __init__(self, source: SourceFile, range: Range) -> None:
        self.source = source
        self.range = range
