from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_group_rules_recognition() -> None:
    m = """
        c1 {    
            group {'x'}
            group g1 {'y'}
            uncaptured group {'y'}
            uncaptured group g2 {'y'}
        }

        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"(x)(y)(?:y)(?:y)"

def test_lookaround_nested_form() -> None:
    m = """
        c {
            starts
            maybe one of 'something2' group {'x'}
            lookbehind 'x' uncaptured group {'y'} lookahead 'y'
            ends
        }
 
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^([something2])?(x)(?<=x)(?:y)(?=y)$"

def test_lookaround_group_name() -> None:
    m = """
        c {
            starts
            maybe one of 'something2' group g1 {'x'}
            group g2 {letter}
        }

        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^([something2])?(x)([A-Za-z])"

