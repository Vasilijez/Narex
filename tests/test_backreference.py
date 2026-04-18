from narex import get_metamodel
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

    mm = get_metamodel()
    m = mm.model_from_str(m)
    e = PythonEngine()
    r = e.generate(m)


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
        mm = get_metamodel()
    except Exception as e:
        assert isinstance(e, TextXSemanticError)