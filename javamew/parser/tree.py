
from typing import List, TypeAlias, Union
from .ast import Node

# ------------------------------------------------------------------------------

TypeName = TypeAlias[str]

class CompilationUnit(Node):
    pass


TopLevelClassOrInterfaceDeclaration = TypeAlias[Union["ClassDeclaration", "InterfaceDeclaration"]]

class OrdinaryCompilationUnit(CompilationUnit):
    package: "PackageDeclaration"
    imports: List["ImportDeclaration"]
    declarations: List[TopLevelClassOrInterfaceDeclaration]

class ModularCompilationUnit(CompilationUnit):
    imports: List["ImportDeclaration"]
    module_declaration: "ModuleDeclaration"

class ModuleDeclaration(Node):
    pass

# ------------------------------------------------------------------------------

class ImportDeclaration(Node):
    pass

class SingleTypeImportDeclaration(ImportDeclaration):
    type_name: TypeName

class TypeImportOnDemandDeclaration(ImportDeclaration):
    type_name: TypeName

class SingleStaticImportDeclaration(ImportDeclaration):
    type_name: TypeName

class StaticImportOnDemandDeclaration(ImportDeclaration):
    type_name: TypeName

# ------------------------------------------------------------------------------

class Annotation(Node):
    pass

class NormalAnnotation(Annotation):
    name: str
    element_values = List["ElementValuePair"]

class MarkerAnnotation(Node):
    pass

class SingleElementAnnotation(Node):
    pass

# ------------------------------------------------------------------------------
PackageModifier = TypeAlias["Annotation"]
class PackageDeclaration(Node):
    modifiers: List["PackageModifier"]
    name: str

# ------------------------------------------------------------------------------

class ClassDeclaration(Node):
    pass

class NormalClassDeclaration(ClassDeclaration):
    pass

class EnumDeclaration(ClassDeclaration):
    pass

class RecordDeclaration(ClassDeclaration):
    pass

# ------------------------------------------------------------------------------

class InterfaceDeclaration(Node):
    pass

# ------------------------------------------------------------------------------
