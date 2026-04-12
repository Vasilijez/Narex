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
    
    class Maybe:
        @staticmethod
        def start():
            return "("

        @staticmethod
        def end():
            return ")?"

    class Either:
        @staticmethod
        def start():
            return "("
        
        @staticmethod
        def separator():
            return "|"

        @staticmethod
        def end():
            return ")"
        
    def interpret_one_of(self, o) -> str:
        return f"[{o.set}]"

    def interpret_domain(self, d) -> str:

        if d.negation:
            self.regex = self.Not.start() + self.regex
        
        if d.type in bounded_domain:
            self.regex += self.BoundedDomain.intepret(d)
        elif d.type in simple_domain:
            self.regex += self.SimpleDomain.intepret(d)
        
    def interpret_repeat(self, r) -> str:
        # The case where  we have only  `n times`  expression.
        if r.end is None:
            return "{" + f"{r.start}" + "}"                   

        # The case where we  have `n1 to n2 times` expression.
        if r.end.type.__class__.__name__:
            return "{" + f"{r.start}" + "," + f"{r.end.value}" + "}"

        # The case where we have `n or more times` expression.
        return "{" + f"{r.start}" + ",}"

    def interpret_either(self, r) -> str:
        self.regex += PythonEngine.Either.start()

        for a in r.alternatives:
            self.interpret_rule(a)
            self.regex += PythonEngine.Either.separator()

        # Trim the extra separator (`|`) character.
        self.regex = self.regex[:-1]
        
        self.regex += PythonEngine.Either.end()

    def interpret_starts(self, r) -> str:
        return "^"
    
    def interpret_rule(self, r) -> str:

        # if debug == True:
        #     print(f"r.type.__class__.__name__ {r.type.__class__.__name__}")
        if r.maybe:
            self.regex += PythonEngine.Maybe.start()

        match r.type.__class__.__name__:
            case 'OneOf':
                self.regex = self.regex + self.interpret_one_of(r.type)
            case 'Domain':
                self.interpret_domain(r.type)
            case 'Either':
                self.interpret_either(r.type)
            
        match r.type:
            case 'starts':
                self.regex += self.interpret_starts(r.type)

        #2 Repeat
        if r.repeat:
            self.regex += self.interpret_repeat(r.repeat)

        #3 `Maybe` rule should  be  processed  at the end
        # as it will encompass whole regular expression.
        if r.maybe:
            self.regex += PythonEngine.Maybe.end()

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