from narex import get_metamodel
from narex.generators.python import generate

def test_either():
    m = """
        clause1:
            one of 'something' either letter or letter or one of 'something2' letter

        clause2
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)