from narex import load_metamodel_and_model_str
from narex import PythonEngine

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
    r = e.generate(m, cli_only=True)
    assert r == r"@\.com\d\/\.\d\.[A-Za-z]"

def test_literal_strange_parenthesis():
    m = """
        head {
            "vasa" '"' "'" 
        }

        target:
            head
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == "vasa\"'"
