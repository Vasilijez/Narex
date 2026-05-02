from narex import load_metamodel_and_model_str
from narex.generators.python import PythonEngine
from textx import TextXSemanticError

def test_backreference_correct_group_name():
    m = """
        c1 {
            group g1 of digit repeat 1 or more times
            'test'
        }

        c2 {
            backreference g1
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
    regex = e.generate(m, cli_only=True)
    assert regex == r"(\d{1,})test\1"

# test_backreference(): bad case when the group doesn't exist

def test_backreference_missing_group_name():
    m = """
        c1 {
            group g1 of digit repeat 1 or more times
            'test'
        }

        c2 {
            backreference missing_group_name
        }

        c { 
            c1
            c2
        }

        target:
            c
    """
    try:
        mm, m = load_metamodel_and_model_str(m)
    except Exception as e:
        assert isinstance(e, TextXSemanticError)