"""
    Use natural language to generate regular expressions.
"""

# Useful for cleaner importing
from narex.utils.loader import load_metamodel_and_model_path
from narex.utils.loader import load_metamodel_and_model_str
from narex.utils.loader import get_metamodel
from narex.generators.python import PythonEngine
from narex.grammar import GRAMMAR_PATH

import os
NAREX_DIR = os.path.dirname(os.path.abspath(__file__))

__version__ = "1.0.2"

__all__ = [
    'load_metamodel_and_model_path', 
    'load_metamodel_and_model_str',
    'get_metamodel',
    'PythonEngine',
    'GRAMMAR_PATH'
]