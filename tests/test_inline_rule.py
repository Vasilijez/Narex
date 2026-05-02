from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_inline_rule():
    m = """
        clause1 {
            one of 'something' letter
            maybe one of 'something2' maybe letter  maybe one of 'something3'
        }

        clause2 {
            one of 'yey' letter
            one of 'wewe' maybe letter  maybe one of 'popopo'
        }

        target:
            clause2
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[yey][A-Za-z][wewe]([A-Za-z])?([popopo])?"