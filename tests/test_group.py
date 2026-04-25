from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_group_rules_recognition():
    m = """
        c1 {    
            group 'x'
            group g1 of 'y'
            uncaptured group 'y'
            uncaptured group g2 of 'y'
        }

        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"(x)(y)(?:y)(?:y)"

def test_lookaround_nested_form():
    m = """
        c {
            starts
            maybe one of 'something2' group 'x'
            lookbehind 'x' uncaptured group 'y' lookahead 'y'
            ends
        }
 
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"^([something2])?(x)(?<=x)(?:y)(?=y)$"

def test_lookaround_group_name():
    m = """
        c {
            starts
            maybe one of 'something2' group g1 of 'x'
            group g2 of letter
        }

        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"^([something2])?(x)([A-Za-z])"

