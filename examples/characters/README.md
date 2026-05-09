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
    SKIP:  ^
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

target:
      match