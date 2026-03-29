from narex import get_metamodel
from narex.generators.python import generate

def test_starts():
    m = """
        c:
            starts maybe one of 'something2' maybe letter  maybe one of 'something3'
        c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_ends():
    m = """
        c:
            starts
            maybe one of 'something2' maybe letter  maybe one of 'something3' 
            ends
        c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

