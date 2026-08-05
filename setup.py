import os
from setuptools import Extension, find_packages, setup
from Cython.Build import cythonize

# Ensure paths are relative to this file's directory.
here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

ext_modules = [
    Extension(
        "pyqterm._parser",
        sources=["pyqterm/parser.pyx"],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "pyqterm._screen_fast",
        sources=["pyqterm/_screen_fast.pyx"],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "pyqterm._render_fast",
        sources=["pyqterm/_render_fast.pyx"],
        extra_compile_args=["-O3"],
    ),
]

setup(
    packages=find_packages(include=["pyqterm", "pyqterm.*"]),
    ext_modules=cythonize(ext_modules, language_level="3"),
)
