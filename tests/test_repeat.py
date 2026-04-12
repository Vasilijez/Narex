from narex import get_metamodel
from narex.generators.python import generate
from textx import TextXSyntaxError    

def test_repeat_something_or_more():
    m = """
    c1 {
        letter repeat 1 or more times
    }

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
    c1 {
        letter repeat 7 times
    }

    c2 {
        maybe one of 'something2' repeat 0 or more times maybe letter  maybe one of 'something3'
    }

    target:
        c1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_repeat_invalid_missing_subject_rule():
    m = """
    c1 {
        maybe repeat 99 times
    }
    
    target:
        c1
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_start_and_end_valid_cases():
    m = """
    c {
        repeat 1 times
        repeat 2 times
        repeat 1 to 2 times
        repeat 1 to 15 times
        repeat 0 or more times
        repeat 1 or more times
        repeat 2 or more times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_0_times():
    m = """
    c {
        repeat 0 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_0_to_0_times():
    m = """
    c {
        repeat 0 to 0 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_start_bigger_than_end():
    m = """
    c {
        repeat 5 to 1 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_negative_start():
    m = """
    c {
        repeat -1 to 0 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_both_negative():
    m = """
    c {
        repeat -1 to -1 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_2_to_2_times():
    m = """
    c {
        repeat -1 to 0 times
    }
    
    target:
        c
    """
    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

