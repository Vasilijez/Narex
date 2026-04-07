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

def validate_domain(domain):
    if domain.between is None:
        return
    
    start = domain.between.start
    end = domain.between.end

    match domain.type:

        case 'digit':
            try:
                # `start` and `end` are automatically assigned properly as 
                # integer values to created object of `Between` class  by textX.
                domain.between.start = int(start)
                domain.between.end = int(end)
            except Exception:
                raise TextXSemanticError("You can't use a non-digit value for `start` or `end` in `between`, if rule is `digit`!")

        case 'small_letter':
            if ('a' <= start <= 'z' and 'a' <= end <= 'z') == False:
                raise TextXSemanticError("You can't use a non-small-letter value for `start` or `end` in `between`, if rule is `small_letter`!")

        case 'big_letter':
            if ('A' <= start <= 'Z' and 'A' <= end <= 'Z') == False:
                raise TextXSemanticError("You can't use a non-big-letter value for `start` or `end` in `between`, if rule is `big_letter`!")

