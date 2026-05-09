from narex import load_metamodel_and_model_str
from narex import PythonEngine
from textx import TextXSyntaxError    

def test_repeat_something_or_more() -> None:
    m = """
    c1 {
        letter repeat 1 or more times
    }

    target:
        c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[A-Za-z]{1,}"

# error
# maybe...one of and then repeat?!
def test_repeat_something_times() -> None:
    m = """
    c1 {
        letter repeat 7 times
    }

    c2 {
        maybe one of 'something2' repeat 1 or more times maybe letter  maybe one of 'something3'
    }

    target:
        c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[A-Za-z]{7}"

def test_repeat_invalid_missing_subject_rule() -> None:
    m = """
    c1 {
        maybe repeat 99 times
    }
    
    target:
        c1
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_start_and_end_valid_cases() -> None:
    m = """
    c {
        digit repeat 1 times
        digit repeat 2 times
        digit repeat 1 to 2 times
        digit repeat 1 to 15 times
        digit repeat 0 or more times
        digit repeat 1 or more times
        digit repeat 2 or more times
    }
    
    target:
        c
    """
    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\d{1}\d{2}\d{1,2}\d{1,15}\d{0,}\d{1,}\d{2,}"

def test_repeat_invalid_0_times() -> None:
    m = """
    c {
        repeat 0 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_0_to_0_times() -> None:
    m = """
    c {
        repeat 0 to 0 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_start_bigger_than_end() -> None:
    m = """
    c {
        repeat 5 to 1 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_negative_start() -> None:
    m = """
    c {
        repeat -1 to 0 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_both_negative() -> None:
    m = """
    c {
        repeat -1 to -1 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

def test_repeat_invalid_2_to_2_times() -> None:
    m = """
    c {
        repeat -1 to 0 times
    }
    
    target:
        c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)
