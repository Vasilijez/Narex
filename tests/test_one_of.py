from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_one_of_special_chars_and_non_special_combined() -> None:
    m = """
        c {
            one of "'.]"
        }

        target: c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"['.\]]"

def test_one_of_special_chars_only() -> None:
    m = """
        c {
            one of "-'^!.$[]"
        }

        target: c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[\-'\^!.$\[\]]"
