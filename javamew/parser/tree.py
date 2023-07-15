
from typing import List, Literal, TypeAlias, Union
from .ast import Node

# ------------------------------------------------------------------------------

TypeName = TypeAlias[str]
PackageName = TypeAlias[str]
ModuleName = TypeAlias[str]
PackageOrTypeName = TypeAlias[str]

AmbiguousName = TypeAlias[str]

RequiresModifier = Literal["transitive", "static"]

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
    annotations: List["Annotation"]
    name: str
    module_directives: List["ModuleDirective"]

# ------------------------------------------------------------------------------

class ModuleDirective(Node):
    pass

class RequiresModuleDirective(ModuleDirective):
    modifier = RequiresModifier
    module_name = ModuleName

class ExportsModuleDirective(ModuleDirective):
    package_name: PackageName
    to_modules: List[ModuleName]


class OpensModuleDirective(ModuleDirective):
    package_name: PackageName
    to_modules: List[ModuleName]


class UsesModuleDirective(ModuleDirective):
    type_name: TypeName

class ProvidesModuleDirective(ModuleDirective):
    type_name: TypeName
    with_types: List[TypeName]

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

ClassModifier = TypeAlias[Literal["public", "protected", "private", "abstract", "static", "final", "sealed", "non-sealed", "strictfp"]]

class NormalClassDeclaration(ClassDeclaration):
    annotations: List[Annotation]
    modifiers: List[ClassModifier]
    name: str
    generic_parameters: List["TypeParameter"]
    extends: "ClassType"
    interfaces: List["InterfaceType"]
    permits: List[TypeName]
    body: List["ClassBodyDeclaration"]

class EnumDeclaration(ClassDeclaration):
    pass

class RecordDeclaration(ClassDeclaration):
    pass

# ------------------------------------------------------------------------------

class InterfaceDeclaration(Node):
    pass

# ------------------------------------------------------------------------------
