from narex import get_metamodel
from narex.generators.python import generate
from textx import TextXSyntaxError    

def test_repeat_something_or_more():
    m = """
    c1:
        letter repeat 1 or more times
    
    target:
        c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

# error
# maybe...one of and then repeat?!
def test_repeat_something_times():
    m = """
    c1:
        letter repeat 7 times
    c2:
        maybe one of 'something2' repeat 0 or more times maybe letter  maybe one of 'something3'
        
    target:
        c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_repeat_invalid_missing_subject_rule():
    m = """
    c1:
        maybe repeat 99 times

    target:
        c1
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

