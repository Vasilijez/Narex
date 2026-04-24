from narex import get_metamodel
from narex.cli.main import load_metamodel_and_model_str
from narex.generators.python import PythonEngine

def test_literal_many_values_combined():
    m = """
    c {
        '@' 
        '.com'
        digit
        '/' '.' digit '.' letter
    }

    target:
        c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"@\.com\d/\.\d\.[A-Za-z]"
