from narex import get_metamodel
from narex.generators.python import generate


def test_repeat_():
    m = """
    c1:
        letter repeat 1 or more times
    
    c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_repeat_():
    m = """
    c1:
        letter repeat 7 times
    c2:
        maybe one of 'something2' repeat 0 or more times maybe letter  maybe one of 'something3'
        
    c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)
