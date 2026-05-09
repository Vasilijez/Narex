from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_lookaround_rules_recognition() -> None:
    m = """
        c1 {
            lookbehind 'x'
            small_letter between a and z
            lookahead 'x'
        }

        c2 {
            negative lookbehind 'x'
            small_letter between a and z
            negative lookahead 'x'
        }

        c {
            c1
            c2
        }

        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"(?<=x)[a-z](?=x)(?<!x)[a-z](?!x)"

def test_lookaround_nested_form() -> None:
    m = """
        c {
            starts
            maybe one of 'something2' lookahead 'x'
            lookbehind 'x' big_letter between A and C negative lookahead letter
            ends
        }

        target:
            c
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^([something2])?(?=x)(?<=x)[A-C](?![A-Za-z])$"

