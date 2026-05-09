from jinja2 import Environment, FileSystemLoader
import re
import os

#######################
#### Python engine ####
#######################

simple_domain = {
    'space', 'whitespace', 'alphanumeric', 
    'anything', 'letter'
}

bounded_domain = {
    'digit', 'small_letter', 'big_letter'
}

special_chars = {
    '\\', '.', ',', '#', '^', '$', '*', '+', '?', '(', ')', '[', ']', '{', '}', '|', '/'
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
        def interpret(d):
            match d.type:
                case 'space':
                    return " "
                case 'whitespace':
                    return r"\s"
                case 'alphanumeric':
                    return r"\w"
                case 'anything':
                    return "."
                case 'letter':
                    return "[A-Za-z]"
                
    class BoundedDomain:
        @staticmethod
        def without_between(d):
            match d.type:
                case 'digit':
                    return r"\d"
                
                case 'small_letter':
                    return "[a-z]"
                
                case 'big_letter':
                    return "[A-Z]"

        @staticmethod
        def with_between(d):
            return f"[{d.between.start}-{d.between.end}]"
        
        @staticmethod
        def interpret(d):
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
            regex += self.BoundedDomain.interpret(domain)
        elif domain.type in simple_domain:
            regex += self.SimpleDomain.interpret(domain)
        
        if domain.negation:
            regex = regex + self.Not.end()

        return regex

    def interpret_repeat(self, repeat) -> str:
        # The case where  we have only  `n times`  expression.
        if repeat.end is None:
            return "{" + f"{repeat.start}" + "}"                   

        # The case where we  have `n1 to n2 times` expression.
        if repeat.end.value:
            return "{" + f"{repeat.start}" + "," + f"{repeat.end.value}" + "}"

        # The case where we have `n or more times` expression.
        return "{" + f"{repeat.start}" + ",}"

    def interpret_either(self, regex, either) -> str:
        regex += PythonEngine.Either.start()

        for a in either.alternatives:
            regex = self.interpret_rule(regex, a)
            regex += PythonEngine.Either.separator()

        # Trim the extra separator (`|`) character.
        regex = regex[:-1]
        
        regex += PythonEngine.Either.end()

        return regex

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
        # 1. uncaptured group g2 of 'y'  // produced regex alias (as it can't be referenced by `\1`, but it can by `g2`)
        # 2. uncaptured group 'y'        // unproduced ref (none narex ref, however it consumes input and is contained in the match)
        # 3. group 'x'                   // produced unused ref (it can be referenced by `\1`, but it won't, only narex refs are used)
        # 4. group g1 of 'y'             // used produced ref (narex ref)
        # TODO: Regex validations.

        rule_exp = f"{self.interpret_rule('', group.rule)}"

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
                    return rf"{g.rule_exp}"
                else:
                    return rf"\{i+1}"
                
    def interpret_literal(self, literal) -> str:
        # The user is expected not to escape non-literal values.
        escaped_regex = []

        for char in literal.value:
            if char in special_chars:
                # Insert backslash before a special char.
                char = rf"\{char}"
            escaped_regex.append(char)

        merge = ''.join(escaped_regex)

        return merge

    def interpret_clause_reference(self, reference) -> str:
        return self.clauses[reference.value.name]

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
            case 'Literal':
                regex += self.interpret_literal(rule.type)
            case 'ClauseReference':
                regex += self.interpret_clause_reference(rule.type)

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
            for c in clause.clauses:
                self.clauses[c.name] = self.interpret_clause(c)

        for inline_rule in clause.inline_rules:
            # We can have more than one rule in one `InlineRule`.
            for rule in inline_rule.rules:
                regex = self.interpret_rule(regex, rule)

        return regex

    def interpret_flags(self, generate_str: bool = True, flags: List[str] = []) -> int | str:
        flags_str = []
        flags_int = set()

        for flag in flags:
            match flag:
                case 'multiline':
                    flags_str.append("re.MULTILINE")
                    flags_int.add(re.MULTILINE)
                case 'caseinsensitive':
                    flags_str.append("re.IGNORECASE")
                    flags_int.add(re.IGNORECASE)
                case 'singleline':
                    flags_str.append("re.DOTALL")
                    flags_int.add(re.DOTALL)

        combined_flags = 0
        for f in flags_int:
            combined_flags |= f

        if generate_str:
            return " | ".join(flags_str) 
        else:
            return combined_flags

    def create_file(
            self, 
            output_file_path, 
            raw_regex = "", 
            repr_regex = "", 
            model=None, 
            flags=None, 
            tests=None
        ):
        engine_file_dir = os.path.dirname(os.path.abspath(__file__))
        environment = Environment(loader=FileSystemLoader(engine_file_dir))
        template = environment.get_template("templates/python_template.jinja")

        if output_file_path == "":
            output_file_path = os.path.join(engine_file_dir, "out_regex.py")

        template.stream({
            "raw_regex": raw_regex,
            "repr_regex": repr_regex,
            "model": model,
            "flags": flags,
            "tests": tests
        }).dump(output_file_path)

    class TestMatches:
        def __init__(self, pattern, matches):
            self.pattern = pattern 
            self.matches = matches

    def interpret_test(self, test: str, regex: str, flags: int, is_global: bool) -> List[Match[str]] | None:
        if is_global:
            # Already iterable.
            matches = list(re.finditer(regex, test, flags=flags))
            size = len(matches)
            if size == 0:
                return None
            return matches
        else:
            # Make iterable.
            match = re.search(regex, test, flags) 
            if match is None:
                return None
            return [match]

    def interpret_tests(self, tests, regex, flags, is_global) -> list:
        test_matches = []
        for pattern in tests:
            matches = self.interpret_test(pattern, regex, flags, is_global)
            test_matches.append(self.TestMatches(pattern, matches))

        return test_matches

    def generate(self, model, cli_only=False, output_file_path="") -> str:
        for clause in model.clauses:
            regex = self.interpret_clause(clause)
            self.clauses[clause.name] = regex

        result = self.clauses[model.target.clause.name]

        if cli_only == False:
            flags = tests = []
            if model.optional:
                if model.optional.flags:
                    flags = model.optional.flags.values
                if model.optional.tests:
                    tests = model.optional.tests.values

            tests = self.interpret_tests(
                tests,
                regex,
                self.interpret_flags(False, flags),
                "globalmatch" in flags
            )

            self.create_file(
                output_file_path=output_file_path,
                raw_regex=regex,
                repr_regex=repr(regex),  # This escaping is specific only for Python. It is about choosing the best python parethesis combo based upon the regex string.
                model=model,
                flags=self.interpret_flags(True, flags),
                tests=tests
            )

        return result


if __name__ == '__main__':
    ...
		