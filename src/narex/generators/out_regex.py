# Raw regex is:
#  [a-z]

# Selected engine is:
#  Python

# Code generation proposal:
import re

text = ""   # empty
regex = r'[a-z]'


match_strings = re.findall(regex, text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
match_objects = re.finditer(regex, text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)


