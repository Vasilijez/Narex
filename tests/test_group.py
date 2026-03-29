from narex import get_metamodel
from narex.generators.python import generate

def test_group_rules_recognition():
    m = """
        c1:        
            group 'x'
            uncaptured group 'y'

        c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_lookaround_nested_form():
    m = """
        c:
            starts
            maybe one of 'something2' group 'x'
            lookbehind 'x' uncaptured group 'y' lookahead 'y'
            ends
            
        c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

