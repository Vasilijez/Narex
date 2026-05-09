## Match all the coefficients of x²
``` py
""" 
    x³ + x² + x + 1
    3x² - 125x + 12
    2x³ + 5x² + 8x - 15
    6x² + 18 - 35x
    12x³ + 95x² - 115

    MATCH: 3
    MATCH: 5
    MATCH: 6
    MATCH: 95
""" 

variable {
      lookahead 'x²'
}

coefficient {
      digit repeat 1 or more times 
}

monomial {
      coefficient 
      variable
}

flags:
      global match,
      multiline

tests:
      "x³ + 2x² + x + 2",
      "x³ + 3x² + x + 1"

engine: 
      python

target: 
      monomial