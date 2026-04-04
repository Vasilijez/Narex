from narex import get_metamodel
from narex.generators.python import generate

def test_backreference():
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
    r = generate(m)


# test_backreference(): bad case when the group doesn't exist