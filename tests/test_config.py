from narex import load_metamodel_and_model_str
from narex import PythonEngine


def test_config_engine_first() -> None:
    m = """
        clause1 {
            letter
        }
        
        engine:
            python
            
        tests:
            'test1', 'test2'
        
        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[A-Za-z]"

def test_config_tests_first() -> None:
    m = """
        clause1 {
            letter
        }
        
        tests:
            'test1', 'test2'

        engine:
            python

        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[A-Za-z]"


def test_config_flags() -> None:
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
    r = e.generate(m, cli_only=True)
    assert r == r"[A-Za-z]"