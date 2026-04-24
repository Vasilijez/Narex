from narex import get_metamodel
from narex.cli.main import load_metamodel_and_model_str
from narex.generators.python import PythonEngine


def test_optional_flavor_first():
    m = """
        clause1 {
            letter
        }
        
        flavor:
            python
            
        tests:
            'test1', 'test2'
        
        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"[A-Za-z]"

def test_optional_tests_first():
    m = """
        clause1 {
            letter
        }
        
        tests:
            'test1', 'test2'

        flavor:
            python

        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"[A-Za-z]"


def test_optional_flags():
    m = """
        clause1 {
            letter
        }
        
        tests:
            'test1', 'test2'

        flags:
            multiline, case insensitive, single line, global match

        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m)
    assert r == r"[A-Za-z]"