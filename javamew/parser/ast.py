

import pickle

import six
from pydantic import BaseModel

class Node(BaseModel):

    def __init__(self):
        self.attrs = [x for x in dir(self) if not x.startswith('__')]
    
    def __equals__(self, other):
        if type(other) is not type(self):
            return False

        for attr in self.attrs:
            if getattr(other, attr) != getattr(self, attr):
                return False

        return True

    def __repr__(self):
        attr_values = []
        for attr in sorted(self.attrs):
            attr_values.append('%s=%s' % (attr, getattr(self, attr)))
        return '%s(%s)' % (type(self).__name__, ', '.join(attr_values))

    def __iter__(self):
        return walk_tree(self)

    def filter(self, pattern):
        for path, node in self:
            if ((isinstance(pattern, type) and isinstance(node, pattern)) or
                (node == pattern)):
                yield path, node

    @property
    def children(self):
        return [getattr(self, attr_name) for attr_name in self.attrs]


def walk_tree(root: Node):
    children = None

    if isinstance(root, Node):
        yield (), root
        children = root.children
    else:
        children = root

    for child in children:
        if isinstance(child, (Node, list, tuple)):
            for path, node in walk_tree(child):
                yield (root,) + path, node

def dump(ast, file):
    pickle.dump(ast, file)

def load(file):
    return pickle.load(file)
