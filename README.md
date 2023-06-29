# javamew
Javamew is a pure Python library for working with Java source code.
Javamew provides a lexer and parser targeting Java 20.
The implementation is based on the Java language spec available at [Java SE20](http://docs.oracle.com/javase/specs/jls/se20/html/).

The following gives a very brief introduction to using javamew.

---------------
Getting Started
---------------

```python
import javamew
tree = javamew.parse.parse("package javamew.brewtab.com; class Test {}")
```

This will return a ``CompilationUnit`` instance. This object is the root of a tree which may be traversed to extract different information about the compilation unit,
