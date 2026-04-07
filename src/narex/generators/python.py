

#######################
#### Python flavor ####
#######################

regex = ''
clauses = {}
def interpret_one_of(o) -> str:
    return f"[{o.set}]"
def interpret_rule(r) -> str:
    global regex

    # if debug == True:
    #     print(f"r.type.__class__.__name__ {r.type.__class__.__name__}")
        
    match r.type.__class__.__name__:
        case 'OneOf':
            regex += interpret_one_of(r.type)
        case 'Domain':
            regex += intepret_domain(r.type)

    # `Maybe` rule should  be  processed  at the end
    # as it will encompass whole regular expression.
    # if r.maybe:

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