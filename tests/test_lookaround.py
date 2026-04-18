from narex import get_metamodel
from narex.generators.python import PythonEngine

def test_lookaround_rules_recognition():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)


def test_lookaround_nested_form():
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)

