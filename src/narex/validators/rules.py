from textx import TextXSemanticError

from narex.generators.python import PythonEngine

special_chars = {
    '.', ',', '#', '^', '$', '*', '+', '?', '(', ')', '[', ']', '{', '}', '|'
}

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

def validate_repeat(repeat):
    start = repeat.start
    end = None if repeat.end is None else repeat.end.value

    if end is None:
        if start == 0:
            raise TextXSemanticError("You can't `repeat` zero times!") 
        
        if start < 0:
            raise TextXSemanticError("You can't use a negative number in `repeat` rule!") 

    else:
        if start <= -1 or end <= -1:
            raise TextXSemanticError("You can't use a negative number in `repeat` rule!") 

        if start > end:
            raise TextXSemanticError("You can't use higher start value than end value in `repeat` rule!") 

        if start == end:
            raise TextXSemanticError("You can't use the same start and end value in `repeat` rule!") 

def validate_literal(literal):
    # We will escape any unescaped character.
    # TODO: Possibly some edge cases.

    sanitized_regex = ""

    for i, char in enumerate(literal.value):
        if char in special_chars:
            if i-1 >= 0 and literal.value[i-1] == "\\":
                continue
            else:
                # Insert backslash before a special char.
                sanitized_regex = literal.value[:i] + f"\{char}" + literal.value[i:]
        elif char == '\\':
            if i+1 < len(literal.value):
                if literal.value[i+1] in special_chars + {'\\'}:
                    continue
                else:
                    raise TextXSemanticError("You can't use a backslash before a non-special character!")
            else:
                # Insert backslash before backslash (a special char).
                sanitized_regex = literal.value[:i] + '\\'

    if sanitized_regex != "":
        literal.value = sanitized_regex

    # (\d)(?:[A-Za-z])[A-Za-z]

def validate_literals(m, mm):

    # Traverse whole tree and validate literals sequence.
    # We need to validate sequence of literals carefully (more than 
    # literal rule).
    # It is straightforward to validate single literal rule, however, sequence of rule is not at all.
    # Caveat: Sometimes you need to override value of the literal rule.

    class Literal:
        def __init__(self, reference):
            self.reference = reference

    literals_sequence = []

    def interpret_rule(self, regex, rule) -> str:

        if rule.maybe or rule.repeat or rule.type.__class__.__name__ != 'Literal':
            literals_sequence.clear()
            return

        literals_sequence.append(Literal(rule))
        # aa bb
        # aabb
        # \ \
        # \\
        #
        # .. . 
        # \ .
        # \.


    def interpret_clause(self, clause) -> str:
        regex = ""

        if clause.clauses:
            for clause in clause.clauses:
                self.clauses[clause.name] = interpret_clause(clause)

        for inline_rule in clause.inline_rules:
            # We can have more than one rule in one `InlineRule`.
            for rule in inline_rule.rules:
                regex = interpret_rule(regex, rule)

        return regex


    for clause in m.clauses:
        interpret_clause(clause)

# def validate(m):
#     print(f"anchor {m}")
#     for clause in m.clauses:
#         print(f"clause {clause}")

