## Match a valid email format
``` py
"""  
    MATCH: user@gmail.com 
    MATCH: user@gmail.co.uk
    SKIP:  .user@gmail.com
    SKIP:  user!user@gmail.com
    SKIP:  user!user@gmailcom.
"""

user {
      base_case {
          letter repeat 1 or more times
      }

      base_case 
      maybe '.' base_case repeat 1 or more times
}

domain {
      letter repeat 1 or more times
}
      
tld {
      '.' 
      letter repeat 1 or more times
}

email { 
      user
      '@'
      domain
      '.'
      tld
}

target:
      email