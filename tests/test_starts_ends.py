from narex import get_metamodel
from narex.generators.python import PythonEngine

def test_starts():
    m = """
        c {
            starts maybe one of 'something2' maybe letter  maybe one of 'something3'
        }
        
        target:
            c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)

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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)

