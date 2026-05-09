from textx import TextXSemanticError
from typing import Any
from textx.metamodel import TextXMetaModel

def validate_class_reference(m: Any, mm: TextXMetaModel) -> None:
    global_clauses = []
    for clause in m.clauses:
        global_clauses.append(clause.name)
    
    if m.target.clause.name not in global_clauses:
        raise TextXSemanticError("You can't use an inner clause reference as the target clause reference!")

def validate_domain(domain: Any) -> None:
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

def validate_repeat(repeat: Any) -> None:
    start = repeat.start
    end = None
    
    if repeat.end:
        if repeat.end.value:
            end = repeat.end.value
        else:
            end = 'or more'

    if end is None:
        if start == 0:
            raise TextXSemanticError("You can't `repeat` zero times!") 
        
        if start < 0:
            raise TextXSemanticError("You can't use a negative number in `repeat` rule!") 

    elif end == 'or more':
        if start < 0:
            raise TextXSemanticError("You can't use a negative number in `repeat` rule!") 

    else:
        if start <= -1 or end <= -1:
            raise TextXSemanticError("You can't use a negative number in `repeat` rule!") 

        if start > end:
            raise TextXSemanticError("You can't use higher start value than end value in `repeat` rule!") 

        if start == end:
            raise TextXSemanticError("You can't use the same start and end value in `repeat` rule!") 

def validate_literal(literal: Any) -> Any:
    literal.value = literal.value[1:-1]

    if (len(literal.value) == 0):
        raise TextXSemanticError("You can't use empty value for `literal` rule!")

    return literal

# # def validate(m):
#     print(f"anchor {m}")
#     for clause in m.clauses:
#         print(f"clause {clause}")

