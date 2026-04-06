from textx import TextXSemanticError


def validate_literal(v):
    if v.__class__.__name__ == 'Literal':
        if v.value == "example":
            return
    raise TextXSemanticError

def validate_class_reference(m, mm):
    global_clauses = []
    for clause in m.clauses:
        global_clauses.append(clause.name)
    
    if m.target.clause.name not in global_clauses:
        raise TextXSemanticError("You can't use an inner clause reference as the target clause reference!")

def validate(m):
    ...