## Match exact characters
``` py
""" 
    MATCH: one              
    MATCH: two              
    MATCH: three
    MATCH: !    
    MATCH: .    
    MATCH: 3    
    MATCH: 6    
    MATCH: 9
"""

number {
      either 'one' or 'two' or 'three' or one of '369'
}

char {
      one of '!.'
}

match {
      either number or char
}

tests:
      "asdasdsadasonesaagsdgs",
      "one two three",
      "two three",
      "three",
      "vxvcxv",
      "vxvcxv!",
      "vxvcxv.ad",
      "asd.",
      "144555",
      "1443",
      "54456",
      "9"

target:
      match