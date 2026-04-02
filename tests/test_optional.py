from narex import get_metamodel
from narex.generators.python import generate


def test_optional_flavor_first():
    m = """
        clause1:
            letter

        flavor:
            python
            
        tests:
            'test1' 'test2'
        
        target:
            clause1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)


def test_optional_tests_first():
    m = """
        clause1:
            letter

        tests:
            'test1' 
            'test2'

        flavor:
            python

        target:
            clause1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)


def test_optional_flags():
    m = """
        clause1:
            letter

        tests:
            'test1' 
            'test2'

        flags:
            multiline
            case insensitive
            single line
            global match

        target:
            clause1
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)