# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
import os
from setuptools import Extension, find_packages, setup
from Cython.Build import cythonize

# Ensure paths are relative to this file's directory.
here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

ext_modules = [
    Extension(
        "pyqtermx._parser",
        sources=["pyqtermx/parser.pyx"],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "pyqtermx._screen_fast",
        sources=["pyqtermx/_screen_fast.pyx"],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "pyqtermx._render_fast",
        sources=["pyqtermx/_render_fast.pyx"],
        extra_compile_args=["-O3"],
    ),
]

setup(
    packages=find_packages(include=["pyqtermx", "pyqtermx.*"]),
    ext_modules=cythonize(ext_modules, language_level="3"),
)
