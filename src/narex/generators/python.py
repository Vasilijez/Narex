import string

#######################
#### Python flavor ####
#######################

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

    class Digit:
        @staticmethod
        def without_between():
            return "\d"

        @staticmethod
        def with_between(start, end):
            return f"[{start}-{end}]"

    def interpret_one_of(self, o) -> str:
        return f"[{o.set}]"

    def intepret_domain(self, d) -> str:

        if d.negation is not None:
            self.regex = self.Not.start() + self.regex
        
        match d.type:
            case 'digit':
                if d.between is None:
                    self.regex = self.regex + self.Digit.without_between()
                else:               
                    self.regex = self.regex + self.Digit.with_between(
                            d.between.start, 
                            d.between.end
                        )
        
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