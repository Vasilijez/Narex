from narex import get_metamodel
from narex.generators.python import generate

def test_group_rules_recognition():
    m = """
        c1:        
            group 'x'
            group g1 of 'y'
            uncaptured group 'y'
            uncaptured group g2 of 'y'

        target:
            c1
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
            
        target:
            c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_lookaround_group_name():
    m = """
        c:
            starts
            maybe one of 'something2' group g1 of 'x'
            group g2 of letter
            
        target:
            c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

