from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "*",
        sources=["javamew/*/*.py"],
        language="c++",
        libraries=[],
    )
]


setup(
    name="javamew",
    ext_modules=cythonize(
        extensions,
        language_level = "3",
        annotate=True,
        compiler_directives={'language_level' : "3"}, 
    ),

)
