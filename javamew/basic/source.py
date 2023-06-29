

import cython

@cython.cclass
class SourcePosition:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column


@cython.cclass
class SourceRange:
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
