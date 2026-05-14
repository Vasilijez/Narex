from narex import load_metamodel_and_model_str
from narex import PythonEngine
from textx import TextXSemanticError

def test_simple_boundary_usage() -> None:
    m = """
        c {
            boundary
            digit
            letter
            boundary
        }
        
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\b\d[A-Za-z]\b"

def test_when_boundary_is_used_with_repeat() -> None:
    m = """
        c {
            boundary repeat 1 or more times
        }
        
        target:
            c
    """

    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

