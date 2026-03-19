from narex import get_metamodel
from narex.generators.python import generate

def test_literal():
    m = """
        'example'
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)

    assert r == "Python regex"
