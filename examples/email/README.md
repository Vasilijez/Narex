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
      username {
          letter repeat 1 or more times
      }
      extended_username {
          '.' username 
      }

      username
      uncaptured group {
            extended_username
      } repeat 0 or more times
}

domain {
      letter repeat 1 or more times
}
      
tld {
      '.' 
      letter repeat 1 or more times
}

tlds {
      group {tld} repeat 1 or more times
}

email { 
      starts
      user
      '@'
      domain
      tlds
      ends
}

tests:
      "user@gmail.com",
      "user@gmail.co.uk",
      ".user@gmail.com",
      "user!user@gmail.com",
      "user!user@gmailcom."

target:
      email