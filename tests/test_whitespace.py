from narex import get_metamodel
from narex.generators.python import generate

def test_whitespace():
    m = """
        c1:
            whitespace repeat 1 or more times
        c2:
            letter whitespace
        
        c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)