

#######################
#### Python flavor ####
#######################

regex = ''
clauses = {}
def interpret_clause(c) -> str:
    if c.clauses:
        for clause in c.clauses:
            clauses[clause.name] = interpret_clause(c)

    for inline_rule in c.inline_rules:
        # We can have more than one rule in one `InlineRule`.
        for rule in inline_rule.rules:
            interpret_rule(rule)

def generate(model) -> str:
    for clause in model.clauses:
        print(f"clause {clause}")
        interpret_clause(clause)

    return f"Python regex"


if __name__ == '__main__':
    ...