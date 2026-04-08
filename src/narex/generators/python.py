import string

#######################
#### Python flavor ####
#######################

simple_domain = {
    'space', 'whitespace', 'alphanumeric', 
    'anything', 'letter'
}

bounded_domain = {
    'digit', 'small_letter', 'big_letter'
}

class PythonEngine:
    
    def __init__(self):
        self.regex = ''
        self.clauses = {}

    class Not:
        @staticmethod
        def start():
            return "[^"

        @staticmethod
        def end():
            return "]"

    class SimpleDomain:
        @staticmethod
        def intepret(d):
            match d.type:
                case 'space':
                    return " "
                case 'whitespace':
                    return "\s"
                case 'alphanumeric':
                    return "\w"
                case 'anything':
                    return "."
                case 'letter':
                    return "[A-Za-z]"
                
    class BoundedDomain:
        @staticmethod
        def without_between(d):
            match d.type:
                case 'digit':
                    return "\d"
                
                case 'small_letter':
                    return "[a-z]"
                
                case 'big_letter':
                    return "[A-Z]"

        @staticmethod
        def with_between(d):
            return f"[{d.between.start}-{d.between.end}]"
        
        @staticmethod
        def intepret(d):
            if d.between is None:
                return PythonEngine.BoundedDomain.without_between(d)
            return PythonEngine.BoundedDomain.with_between(d)


    def interpret_one_of(self, o) -> str:
        return f"[{o.set}]"

    def intepret_domain(self, d) -> str:

        if d.negation is not None:
            self.regex = self.Not.start() + self.regex
        
        if d.type in bounded_domain:
            self.regex += self.BoundedDomain.intepret(d)
        elif d.type in simple_domain:
            self.regex += self.SimpleDomain.intepret(d)
        
    def interpret_rule(self, r) -> str:

        # if debug == True:
        #     print(f"r.type.__class__.__name__ {r.type.__class__.__name__}")
            
        match r.type.__class__.__name__:
            case 'OneOf':
                self.regex = self.regex + self.interpret_one_of(r.type)
            case 'Domain':
                self.intepret_domain(r.type)

        # `Maybe` rule should  be  processed  at the end
        # as it will encompass whole regular expression.
        # if r.maybe:

    def interpret_clause(self, c) -> str:
        if c.clauses:
            for clause in c.clauses:
                self.clauses[clause.name] = self.interpret_clause(c)

        for inline_rule in c.inline_rules:
            # We can have more than one rule in one `InlineRule`.
            for rule in inline_rule.rules:
                self.interpret_rule(rule)

    def generate(self, model) -> str:

        for clause in model.clauses:
            self.interpret_clause(clause)

        return f"Python regex is \n{self.regex}"


if __name__ == '__main__':
    ...