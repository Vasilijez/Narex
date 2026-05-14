## Match a simple number
``` py
""" 
    MATCH: 1000 
    MATCH: 99
    SKIP:  0 
"""

non_zero_digit {
      digit between 1 and 9 
}

number {
      non_zero_digit repeat 1 or more times
      digit repeat 0 or more times
}

tests:
      "1000",
      "99",
      "0"

target:
      number