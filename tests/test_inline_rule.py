from narex import get_metamodel
from narex.generators.python import generate

def test_inline_rule():
    m = """
        clause1:
            one of 'something' letter
            maybe one of 'something2' maybe letter  maybe one of 'something3'

        clause2:
            one of 'yey' letter
            one of 'wewe' maybe letter  maybe one of 'popopo'
        
        clause2
    """

    mm = get_metamodel()
    m = mm.model_from_str(m)
    r = generate(m)