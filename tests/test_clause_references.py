from narex import get_metamodel
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)

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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)


def test_clause_references_illegal_keywords():
    mm = get_metamodel()

    m = """
        c {
            digit
            target
        }

        target:
            c
    """
    try:
        m = mm.model_from_str(m)
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
        m = mm.model_from_str(m)
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
        m = mm.model_from_str(m)
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
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)
