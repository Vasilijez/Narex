## Match various date formats and capture the year
``` py

""" 
    MATCH: 04/06/25    CAPTURE: 25
    MATCH: 18/12/05    CAPTURE: 05           
    MATCH: 25/05/1998  CAPTURE: 1998     
    SKIP:  99/99/9999
"""

month {
      either '0' or '1'
      digit between 0 and 2
}

day {
      digit between 0 and 3
      digit
}

year {
      short_format {
          digit repeat 2 times
      }

      long_format {  
          digit repeat 4 times
      }

      either short_format or long_format
}

date {
      day
      '/'
      month
      '/'
      group year
}

target:
      date