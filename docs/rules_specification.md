# Rules:

### Clause
Defines a reusable sub-regex block.
``` yml
name { 
      [clauses] 
      rules 
}
```
- `name` the clause identifier.
- `[clauses]` zero or more sub-clauses.
- `rules` one or more rules.
``` yml
email { 
      name {
            'John'
      }
      digit repeat 3 times 
}
```
### Rule
Defines a single regex rule.
``` yml
[maybe] <rule_type> [repeat] 
```
- `[maybe]` non-mandatory keyword representing the optionality of a rule.
- `<rule_type>` one of the following rules `one of | domain | either | starts | ends | boundary | lookaround | group | backreference | literal | clause reference`
- `[repeat]` non-mandatory setting used to describe repetition.
``` yml
maybe digit repeat 1 or more times
```
### Repeat
An optional setting which representing how many times a rule will repeat.
``` yml
repeat <start_val> [or more | to <end_val>] times
```
- `repeat` keyword marking the start of the repetition block.
- `<start_val>` represents the minimum number of repetitions.
- `or more` non-mandatory keywords representing an unbounded maximum.
- `to <end_val>` non-mandatory setting defining the maximum number of repetitions.
- `times` a reserved keyword.
``` yml
letter repeat 1 or more times
digit repeat 1 to 2 times
big_letter repeat 3 times
```
### One of
Creates a character set, matching any single character contained within the provided string.
``` yml
one of <string_set>
```
- `one of` reserved keywords.
- `<string_set>` a string containing all characters to be included in the set.
``` yml
one of "abc"
one of "@#$%"
```
### Either
Defines an alternation between two or more rules, where any of the provided patterns can match.
``` YAML
either <rule> [[or <rule>] | ...]
```
- `either` keyword marking the start of the choice.
- `or` reserved keyword used to separate alternative rules.
- `<rule>` any valid rule.
``` yml
either digit
either 'http' or 'https'
either digit or c1
```
### Starts / ends
Asserts that the rule must occur at a specific boundary of the text.
``` YML
starts
```
- `starts` asserts the pattern begins at the start of a line or string.
``` YML
ends
```
- `ends` asserts the pattern concludes at the end of a line or string.
``` YAML
starts 'Login'
digit repeat 5 times ends
starts digit ends
```
### Boundary
Asserts a word boundary position where a word character is not followed or preceded by another word character.
``` YML
boundary
```
- `boundary` reserved keyword representing the position between a word and a non-word character.
``` YAML
boundary 'word'
'cat' boundary
```

### Lookaround
Assertions that check if a rule exists (or doesn't exist) before or after the current position without consuming the text.
```yml
[negative] lookahead | lookbehind <rule>
```
* `[negative]` non-mandatory keyword that inverts the logic (ensures the rule does not match).
* `lookahead` checks the context after the current position.
* `lookbehind` checks the context before the current position.
* `<rule>` the pattern to be checked.

Matches 'apple' only if followed by a space.
```yml
'apple' lookahead space
```
Matches 'price' only if not preceded by a dollar sign.
``` yml
negative lookbehind '$' 'price'
```

### Group
Wraps one or more rules into a single unit for logical grouping or data extraction.
```yml
[uncaptured] group [name] { rules }
```

* `[uncaptured]` non-mandatory keyword that prevents the group from being stored as a group result.
* `[name]` non-mandatory identifier used to refer group.
* `{ rules }` the block which holds at least one rule.

```yml
group user_id { digit repeat 5 times }
uncaptured group { either 'cat' or 'dog' }
```

### Backreference
Matches the exact same text (not just satisfying regex pattern!) that was previously matched by a named group. 
```yml
backreference <group_name>
```
* `backreference` reserved keyword.
* `<group_name>` the name of the group you want to repeat.
```yml
group quote { '"' } letter repeat 1 or more times 
backreference quote
```
If you still don't understand, check [examples](../examples/) directory.

### Domain

Defines specific categories of characters to match. Domains can be negated or restricted to a specific range.

```yml
[not] <domain_type> [between <start> and <end>]
```

* `[not]` optional keyword that inverts the selection.
* `<domain_type>` the category of characters (see below).
* `[between <start> and <end>]` optional range restriction for bounded domains.

#### Simple domains

These domains represent broad categories and do not support range restrictions.

* `space` matches a single space character.
* `whitespace` matches any whitespace (tabs, newlines, spaces).
* `alphanumeric` matches letters, digits and `_` (useful for variables).
* `letter` matches any uppercase or lowercase letter.
* `anything` matches any single character.

#### Bounded domains

These domains represent ordered arrays and can be used with the `between` keyword.

* `digit` matches numeric characters (0-9).
* `small_letter` matches lowercase letters (a-z).
* `big_letter` matches uppercase letters (A-Z).

```yml
digit between 1 and 5
not small_letter
small_letter between a and f
```

### Literal
Matches a specific, exact string of characters. This is the most basic rule type for matching fixed text.
```yml
'string' | "string"

```
* `'string'` / `"string"` represents the exact text to match, enclosed in single or double quotes.
```yml
'https://'
"user_name"
'.'
"@"
'email'
```

### Clause reference
Allows you to reuse a previously defined clause by its name. This keeps your code modular and readable by breaking complex expressions into smaller, named parts.
```yml
<clause_name>
```
* `<clause_name>` must match the identifier of a clause defined earlier in the file.

```yml
area_code { 
    digit repeat 3 times 
}

phone_number { 
    area_code 
    '-' 
    digit repeat 7 times 
}
```

### Config
Global settings used to configure the regex engine, define test cases, and set execution flags.
```yml
tests: "val1", "val2"
engine: <engine_type>
flags: <flag1>, <flag2>
```
* `tests` an optional comma-separated list of strings to validate the regex against.
* `engine` an optional setting which specifies the regex flavor (e.g. `python`).
* `flags` an optional setting which modifies matching behavior (e.g., `case insensitive`, `global match`, `multiline`, `single line`).
```yml
tests: "John123", "Doe456"
engine: python
flags: case insensitive, global match
```

### Target
The mandatory entry point that tells Narex which clause to use as the final regular expression.
```yml
target: <clause_name>
```
* `target` reserved keyword.
* `<clause_name>` the name of the main clause to be generated. Whatever clause can be used.
```yml
target: email
```

## Notes

### Literal escaping
The user shouldn't perform any escaping of literals, as this could produce an inaccurate regex. Each literal enclosed in `''` will be escaped individually (e.g. `'!@'`). If the user provides two consecutive literal rules (e.g. `'@'` and `'.com'`), they will not be merged and escaped together.
### Literal quotes
The user shouldn't use double quotes `"` more than twice when defining a literal value (e.g. wrong `""@"`, correct `"@"`). Similarly, the user shouldn't use single quotes `'` more than twice when defining a literal value (e.g. wrong `''@'`, correct `'@'`).
