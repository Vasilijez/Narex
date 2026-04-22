# Raw regex is:
#  [a-z]

# Selected engine is:
#  Python

# Code generation proposal:
import re

text = ""   # empty
regex = r'[a-z]'


# prepare flags
#if re.multiline:
#    flags.append



match_object = re.search(regex, text)


