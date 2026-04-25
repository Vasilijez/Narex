from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_either():
    m = """
        clause1 {
            one of 'something' either letter or letter or one of 'something2' letter
        }

        target:
            clause1
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, only_regex=True)
    assert r == r"[something]([A-Za-z]|[A-Za-z]|[something2])[A-Za-z]"