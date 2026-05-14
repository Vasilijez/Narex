## Match a file with the correct format
``` py
"""
MATCH: fajl_v1.pdf 
MATCH: fajl_v2.png
MATCH: fajl_v3.jpeg
SKIP:  random_name.gif
"""

version {
    digit repeat 0 or more times     
}

format {
    either 'png' or 'pdf' or 'jpeg'
}

file {
    boundary
    'fajl_v' 
    version
    '.'
    format
    boundary
}

tests:
    "fajl_v1.pdf",
    "fajl_v2.png",
    "fajl_v3.jpeg",
    "random_name.gif"

target:
    file