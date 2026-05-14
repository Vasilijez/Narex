## Match repeated numbers from the beginning and the end

``` py
""" 
    MATCH: 12asda12
    MATCH: 54asdasd54
    SKIP:  32asdsad43
    SKIP:  43asdsadsa22
"""

# Even though  a  group seems similar to just 
# referencing a previously defined clause, it 
# is not.  It requires the same value matched 
# within the group to be repeated.

head {
      group g1 {digit repeat 1 or more times} 
}

tail {
      backreference g1
}
  
body {
      letter repeat 1 or more times
}

match {
      head 
      body
      tail
}

tests:
      "12asda12",
      "54asdasd54",
      "32asdsad43",
      "43asdsadsa22"

target:
      match
```