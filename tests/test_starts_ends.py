from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_starts():
    m = """
        c {
            starts maybe one of 'something2' maybe letter  maybe one of 'something3'
        }
        
        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"^([something2])?([A-Za-z])?([something3])?"

def test_ends():
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
    r = e.generate(m)
    assert r == r"^([something2])?([A-Za-z])?([something3])?$"

