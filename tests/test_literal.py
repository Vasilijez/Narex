from narex import get_metamodel
from narex.generators.python import generate

def test_literal_many_values_combined():
    m = """
    c {
        '@' 
        '.com'
        digit
        '/' '.' digit '.' letter
    }

    target:
        c
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)
