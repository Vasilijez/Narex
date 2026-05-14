from narex import load_metamodel_and_model_str
from narex import PythonEngine
from textx import TextXSemanticError

def test_starts() -> None:
    m = """
        c {
            starts maybe one of 'something2' maybe letter  maybe one of 'something3'
        }
        
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^([something2])?([A-Za-z])?([something3])?"

def test_when_starts_is_used_with_repeat() -> None:
    m = """
        c {
            starts repeat 1 or more times
        }
        
        target:
            c
    """

    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

def test_ends() -> None:
    m = """
        c {
            starts
            maybe one of 'something2' maybe letter  maybe one of 'something3' 
            ends
        }
        
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^([something2])?([A-Za-z])?([something3])?$"


def test_when_ends_is_used_with_repeat() -> None:
    m = """
        c {
            ends repeat 1 or more times
        }
        
        target:
            c
    """

    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)
