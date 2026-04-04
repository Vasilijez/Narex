from narex import get_metamodel
from narex.generators.python import generate
from textx import TextXSyntaxError, TextXSemanticError

def test_domain_domain_types():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_domain_with_not():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_domain_with_between():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

def test_domain_forbidden_rules_before_between():
    mm = get_metamodel()

    m = """
        c {
            space between 1 and 3
        }

        target:
            c1
    """
    m = mm.model_from_str(m)
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            whitespace between 1 and 3
        }

        target:
            c
    """
    m = mm.model_from_str(m)
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            alphanumeric between 1 and 3
        }

        target:
            c
    """
    m = mm.model_from_str(m)
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)

    m = """
        c {
            anything between 1 and 3
        }

        target:
            c
    """
    m = mm.model_from_str(m)
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSyntaxError)


def test_domain_complex():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)


def test_domain_letter_doesnt_have_between():
    m = """
        c {
            letter between a and z
        }
        
        target:
            c
    """

    mm = get_metamodel()
    try:
        m = mm.model_from_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)

    r = generate(m)

        