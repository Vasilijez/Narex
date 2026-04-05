from textx import TextXSemanticError


def validate_literal(v):
    if v.__class__.__name__ == 'Literal':
        if v.value == "example":
            return
    raise TextXSemanticError

def validate(m):
    ...