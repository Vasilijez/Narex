# Useful for cleaner importing
from narex.utils.loader import load_metamodel_and_model_path
from narex.utils.loader import load_metamodel_and_model_str
from narex.generators.python import PythonEngine

import os
NAREX_DIR = os.path.dirname(os.path.abspath(__file__))
GRAMMAR_PATH = os.path.join(NAREX_DIR, 'grammar.tx')