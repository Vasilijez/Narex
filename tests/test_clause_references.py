from narex import load_metamodel_and_model_str
from narex.generators.python import PythonEngine
from textx import TextXSemanticError

def test_clause_references_simple():
    m = """
        c1 {
            starts
            maybe digit
        }

        c2 {
            letter
            digit
            c1
        }
                
        target:
            c2
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, only_regex=True)
    assert r == r"[A-Za-z]\d^(\d)?"

def test_clause_references_nested():
    m = """
        c1 {
            starts
        }

        c2 {
            digit
        }
        
        c3 {
            letter
        }

        c4 {
            c5 {
                letter
            } 

            c1
            c2
            c3        
            c5
        }
        
        target:
            c4
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, only_regex=True)
    assert r == r"^\d[A-Za-z][A-Za-z]"


def test_clause_references_illegal_keywords():
    m = """
        c {
            digit
            target
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

    m = """
        c {
            digit
            tests
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

    m = """
        c {
            digit
            flavor
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

    m = """
        c {
            digit
            flags
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)
