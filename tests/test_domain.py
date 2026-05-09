from narex import load_metamodel_and_model_str
from narex.generators.python import PythonEngine
from textx import TextXSyntaxError, TextXSemanticError

def test_domain_domain_types() -> None:
    m = """
        c1 {
            digit
            space
            whitespace
            alphanumeric
            anything
            letter
            small_letter
            big_letter
        }

        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\d \s\w.[A-Za-z][a-z][A-Z]"

def test_domain_with_not() -> None:
    m = """
        c1 {
            not whitespace
        }

        c2 {
            not anything not letter
        }

        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[^\s]"

def test_domain_with_between() -> None:
    m = """
        c1 {
            digit between 1 and 3
        }

        c2 {
            letter
        }

        c3 {
            letter
        }
        
        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[1-3]"

def test_domain_forbidden_rules_before_between() -> None:
    m = """
        c {
            space between 1 and 3
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            whitespace between 1 and 3
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            alphanumeric between 1 and 3
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            anything between 1 and 3
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)


def test_domain_complex() -> None:
    m = """
        c1 {
            digit between 1 and 3
        }

        c3 {
            big_letter between A and Z
        }

        c4 {
            small_letter between a and z
            digit between 1 and 9
        }

        target:
            c1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[1-3]"


def test_domain_letter_doesnt_have_between() -> None:
    m = """
        c {
            letter between a and z
        }
        
        target:
            c
    """

    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)


        