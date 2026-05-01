
__version__ = "0.1.0"

# Useful for cleaner importing
from narex.utils.loader import load_metamodel_and_model_path
from narex.utils.loader import load_metamodel_and_model_str
from narex.utils.loader import get_metamodel
from narex.generators.python import PythonEngine
from narex.grammar import GRAMMAR_PATH

import os
NAREX_DIR = os.path.dirname(os.path.abspath(__file__))


