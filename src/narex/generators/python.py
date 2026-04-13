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
        self.groups = []

    class GroupReference:
        def __init__(self, name: str, uncaptured: bool, rule_exp: str = ""):
            self.name = name
            self.uncaptured = uncaptured
            self.rule_exp = rule_exp

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

    def interpret_domain(self, regex, domain) -> str:
        if domain.negation:
            regex = self.Not.start() + regex
        
        if domain.type in bounded_domain:
            regex += self.BoundedDomain.intepret(domain)
        elif domain.type in simple_domain:
            regex += self.SimpleDomain.intepret(domain)
        
        return regex

    def interpret_repeat(self, repeat) -> str:
        # The case where  we have only  `n times`  expression.
        if repeat.end is None:
            return "{" + f"{repeat.start}" + "}"                   

        # The case where we  have `n1 to n2 times` expression.
        if repeat.end.type.__class__.__name__:
            return "{" + f"{repeat.start}" + "," + f"{repeat.end.value}" + "}"

        # The case where we have `n or more times` expression.
        return "{" + f"{repeat.start}" + ",}"

    def interpret_either(self, regex, either) -> str:
        regex += PythonEngine.Either.start()

        for a in either.alternatives:
            self.interpret_rule(regex, a)
            regex += PythonEngine.Either.separator()

        # Trim the extra separator (`|`) character.
        regex = regex[:-1]
        
        regex += PythonEngine.Either.end()

    def interpret_starts(self) -> str:
        return "^"
    
    def interpret_ends(self) -> str:
        return "$"
    
    def interpret_look_ahead(self, regex, lookahead) -> str:
        sign = "!" if lookahead.negative else "="
        regex += "(?" + sign
        regex = self.interpret_rule(regex, lookahead.rule)
        regex += ")"
        return regex

    def interpret_look_behind(self, regex, lookbehind) -> str:
        sign = "!" if lookbehind.negative else "="
        regex += "(?<" + sign
        regex = self.interpret_rule(regex, lookbehind.rule)
        regex += ")"
        return regex
    
    def interpret_group(self, regex, group) -> str:
        # Cases:
        # 1. uncaptured group g2 of 'y'  // produced regex alias
        # 2. uncaptured group 'y'        // unproduced ref
        # 3. group 'x'                   // produced unused ref
        # 4. group g1 of 'y'             // used produced ref
        # TODO: Regex validations.

        rule_exp = f"{self.interpret_rule("", group.rule)}"

        if group.uncaptured:

            # 1.
            if group.name:
                self.groups.append(self.GroupReference(group.name, True, rule_exp))
                return regex + "(?:" + rule_exp + ")"

            # 2.
            else:
                return regex + "(?:" + rule_exp + ")"
            
        else:

            # 3.
            if group.name is None:
                return regex + "(" + rule_exp + ")"
            
            # 4.
            else:
                self.groups.append(self.GroupReference(group.name, False))
                return regex + "(" + rule_exp + ")"

    def interpret_backreference(self, backreference) -> str:
        for i, g in enumerate(self.groups):
            if g.name == backreference.group.name:
                if g.uncaptured:
                    return f"{g.rule_exp}"
                else:
                    return f"\{i+1}"

    def interpret_rule(self, regex, rule) -> str:

        # if debug == True:
        #     print(f"r.type.__class__.__name__ {r.type.__class__.__name__}")
        if rule.maybe:
            regex += PythonEngine.Maybe.start()

        match rule.type.__class__.__name__:
            case 'OneOf':
                regex += self.interpret_one_of(rule.type)
            case 'Domain':
                regex = self.interpret_domain(regex, rule.type)
            case 'Either':
                regex = self.interpret_either(regex, rule.type)
            case 'Lookahead':
                regex = self.interpret_look_ahead(regex, rule.type)
            case 'Lookbehind':
                regex = self.interpret_look_behind(regex, rule.type)
            case 'Group':
                regex = self.interpret_group(regex, rule.type)
            case 'Backreference':
                regex += self.interpret_backreference(rule.type)

        match rule.type:
            case 'starts':
                regex += self.interpret_starts()
            case 'ends':
                regex += self.interpret_ends()
            
        if rule.repeat:
            regex += self.interpret_repeat(rule.repeat)

        # `Maybe` rule should  be  processed  at the end
        # as it will encompass whole regular expression.
        if rule.maybe:
            regex += PythonEngine.Maybe.end()

        return regex

    def interpret_clause(self, clause) -> str:
        regex = ""

        if clause.clauses:
            for clause in clause.clauses:
                self.clauses[clause.name] = self.interpret_clause(clause)

        for inline_rule in clause.inline_rules:
            # We can have more than one rule in one `InlineRule`.
            for rule in inline_rule.rules:
                regex = self.interpret_rule(regex, rule)

        return regex

    def generate(self, model) -> str:
        for clause in model.clauses:
            regex = self.interpret_clause(clause)
            if clause.name == model.target.clause.name:
                break

        return f"Python regex is: \n{regex}"


if __name__ == '__main__':
    ...