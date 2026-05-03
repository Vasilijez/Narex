# Narex

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

If you have ever used regular expressions, then you know how difficult they can be. Some people, when confronted with a problem, think _“I know, I’ll use regular expressions.”_ Now they have two problems [[1]](https://regex.info/blog/2006-09-15/247).

Challenges of using regular expressions:
- Expressions easily become unreadable, as they are extremely dense.
- No standardization or cross-flavor compatibility. Depending on the flavor, it can vary significantly. Supported features and syntax often differ.
- Unnatural pattern memorization. Humans quickly forget the syntax, as it is not intuitive.
- The learning curve is steep, especially for non-tech users. Even though many non-tech users need data processing, regular expressions remain out of reach for them.

The ultimate goal is to produce a DSL that uses natural language and enables cross-flavor compatibility.

The main use case is for the user to define the desired flavor (Perl, Python, etc.) and write a regular expression using natural language. The output will be raw regular expression, which can be directly used within the specified flavor.

This DSL can be widely used by people from different backgrounds, as it uses natural language. Tricky regular expressions are abstracted, and a universal tool for cross-flavor support is provided. Learning this DSL frees you from ever having to remember regular expression syntax again.

The biggest issues are the vast number of flavors, subtle differences, and partially supported advanced features. Due to the complexity of implementing a DSL that handles advanced features and multiple engine flavors, support will be added gradually.

In the beginning, only the Python flavor will be supported, covering its concepts.
Some of the advanced supported concepts include:
- `[uncaptured] group [<name> of]`
- `backreference <group_name>`
- `[negative] lookahead | lookbehind`
- `if then [else]`

A user can also test regular expression by using `tests:`, define desired flags with `flags:`, and specify the desired flavor using `flavor:`.

### Note
#### Literal escaping
The user shouldn't perform any escaping of literals, as this could produce an inaccurate regex. Each literal enclosed in `''` will be escaped individually (e.g. `'!@'`). If the user provides two consecutive literal rules (e.g. `'@'` and `'.com'`), they will not be merged and escaped together.
#### Literal quotes
The user shouldn't use double quotes `"` more than twice when defining a literal value (e.g. wrong `""@"`, correct `"@"`). Similarly, the user shouldn't use single quotes `'` more than twice when defining a literal value (e.g. wrong `''@'`, correct `'@'`).

## Examples
#### Task 1: Match phone number 
``` py
""" 
    MATCH: +381 62 123 4567
    MATCH: 062/123-4567
    MATCH: 062-123-4567
    MATCH: 0621234567
    MATCH: 062 123 4567
    SKIP:  062/123/4567
"""

carrier {
      digit repeat 2 times
}

state {
      '+'
      digit between 1 to 9
      digit repeat 2 to 3 times
      carrier
}

no_state {
      '0'
      carrier
}

local {
      digit repeat 3 times
      maybe '-'
      digit repeat 4 times
}

separator {
      maybe either '/' or '-' or whitespace 
}

phone_number {
      starts
      either state or no_state
      maybe separator
      local
      ends
}

flags:
      global match,
      multiline

flavor:
      python

tests:
      "062/123-4567"

target:
      phone_number 
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  ^(\+[1-9]\d{2,3}\d{2}|0\d{2})(((\/|-|\s))?)?\d{3}(-)?\d{4}$
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
#    test 1:
#      pattern: 062/123-4567
#      match 1: 062/123-4567
#      group 0: 062
#      group 1: /
#      group 2: /
#      group 3: /
#      group 4: -
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '^(\\+[1-9]\\d{2,3}\\d{2}|0\\d{2})(((\\/|-|\\s))?)?\\d{3}(-)?\\d{4}$'

match_strings = re.findall(
    regex, 
    text, 
    flags=re.MULTILINE
    
)
match_objects = re.finditer(
    regex, 
    text, 
    flags=re.MULTILINE
)
```

#### Task 2: Match repeated numbers from head and tail 
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
      group g1 of digit repeat 1 or more times
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

target:
      match
```
Generated code:
``` py
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  (\d{1,})[A-Za-z]{1,}\1
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '(\\d{1,})[A-Za-z]{1,}\\1'


match_object = re.search(
    regex, 
    text
)
```


#### Task 3: Match correct email format
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
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  [A-Za-z]{1,}(\.)?[A-Za-z]{1,}{1,}@[A-Za-z]{1,}\.\.[A-Za-z]{1,}
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '[A-Za-z]{1,}(\\.)?[A-Za-z]{1,}{1,}@[A-Za-z]{1,}\\.\\.[A-Za-z]{1,}'

match_object = re.search(
    regex, 
    text
)
```


#### Task 4: Match all the coefficients of x²
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

flavor: 
      python

target: 
      monomial
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  \d{1,}(?=x²)
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
#    test 1:
#      pattern: x³ + 2x² + x + 2
#      match 1: 2
#
#    test 2:
#      pattern: x³ + 3x² + x + 1
#      match 1: 3
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '\\d{1,}(?=x²)'

match_strings = re.findall(
    regex, 
    text, 
    flags=re.MULTILINE
    
)
match_objects = re.finditer(
    regex, 
    text, 
    flags=re.MULTILINE
    
)
```


#### Task 5: Match various date formats and capture year
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
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  [0-3]\d/(0|1)[0-2]/((\d{2}|\d{4}))
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '[0-3]\\d/(0|1)[0-2]/((\\d{2}|\\d{4}))'

match_object = re.search(
    regex, 
    text
)
```


#### Task 6: Match simple number
``` py
""" 
    MATCH: 1000 
    MATCH: 99
    SKIP:  0 
"""

non_zero_digit {
      digit between 1 to 9 
}

number {
      non_zero_digit repeat 1 or more times
      digit repeat 0 or more times
}

target:
      number
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  [1-9]{1,}\d{0,}
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '[1-9]{1,}\\d{0,}'


match_object = re.search(
    regex, 
    text
)

```

#### Task 7: Match file with correct format
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

target:
      file
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  \$[1-9]{0,}(\.\d{0,})?
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '\\$[1-9]{0,}(\\.\\d{0,})?'


match_object = re.search(
    regex, 
    text
)
```


#### Task 8: Match the price
``` py
""" 
    MATCH: $3.45
    MATCH: $23.32
    MATCH: $400
    SKIP:  €3.44
    SKIP:  $.23
"""

whole_value {
      digit between 1 and 9 repeat 0 or more times
}

decimal_value {
      '.' digit repeat 0 or more times
}

price {
      '$'
      whole_value 
      maybe decimal_value
}

target:
      price
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  \$[1-9]{0,}(\.\d{0,})?
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '\\$[1-9]{0,}(\\.\\d{0,})?'

match_object = re.search(
    regex, 
    text
)
```


#### Task 9: Match exact characters
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
```
Generated code:
``` python
##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  ((one|two|three|[369])|[!.])
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
# No tests defined.
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '((one|two|three|[369])|[!.])'

match_object = re.search(
    regex, 
    text
)
```



#### Task 10: Based upon condition, match number or message
``` py
""" 
    MATCH: enabled 06012345678
    MATCH: disabled 06012345678 disturbing
    MATCH: enabled 06012345678
    MATCH: enabled 06012345678
    SKIP:  123#@$
"""

condition {
      lookbehind 'enabled'
}

read_number {
      digit repeat 1 or more times
}
  
read_message {
      letter repeat 1 or more times
}

match {
      if condition then read_number else read_message
      ends 
}

target:
      match
```


#### Task 11: Are files found?

``` py
"""  
    MATCH: 1 file found?
    MATCH: 2 files found? 
    MATCH: 24 files found? 
    SKIP:  No files found
"""

_whitespaces {
    whitespace repeat 1 or more times
}

number_one {
    '1'
    _whitespaces   
}

condition {
    (lookahead) number_one
}

other_numbers {
    digit between 2 and 9
    digit repeat 1 or more times
    _whitespaces
}

file_found {
    number_one
    'file'
    _whitespaces
    'found?'
}

files_found {  
    other_numbers
    'files'
    _whitespaces
    'found?'
}

match {
    starts
    if condition then file_found else files_found 
}

target:
      match
```



#### Task 12: Match all the positive numbers only
``` py
"""
    10 -25 -35 45
    -150 25 -35 -147
    8 -88 -888 -8888
    -3 -33 -333 -333

    MATCH: 10
    MATCH: 45
    MATCH: 25
    MATCH: 8
""" 

minus_sign {
      negative lookbehind '-' 
}

number {
      digit repeat 1 or more times
}

positive_number {
      boundary 
      minus_sign
      number
}
      
flags:
      global match,
      multiline

flavor:
      python

target:
      positive_number
```


## Structure
```
Narex/
|
├── src/narex/
|         ├── validators/
|         ├── generators/
|         ├── grammar/
|         ├── utils/
|         ├── cli/
|
├── extension/
├── examples/
├── tests/
|
├── .github/workflows/
├── pyproject.toml
├── LICENSE
├── README.md
```
## Getting started:
Prerequsities:
- Python 3

_Check `project.toml` for more info._

#### Regular user workflow

1. Create a virtual environment:
``` sh
python -m venv .venv
```
2. Activate the virtual environment (Windows):
``` sh
.\.venv\Scripts\activate 
```
3. Install dependencies:
``` sh
pip install git+https://github.com/Vasilijez/Narex.git
```
_Pulling of the source code is optional._

#### Developer workflow
1. Clone the project:
``` sh
git clone https://github.com/Vasilijez/Narex.git
```
2. Locate in the project:
``` sh
cd Narex
```
3. Create and activate the virtual environment (Windows): 
``` sh
python -m venv .venv
.\.venv\Scripts\activate
```
5. Install mandatory dependencies:
``` sh
pip install -e .
```
6. Optionally, if developer needs all dependencies (e.g. tests):
``` sh
pip install -e ".[dev]"
```


### Using
Run the project:

i. You can optionally validate the model before running:
``` sh
narex validate --path=<path>
```
ii. You can just run (includes validation):
``` sh
narex run --path=<path> --full
```
__Caveat:__ 
- If you omit the `--path` flag, then the default model is loaded from `examples` folder.
- The path flag supports both absolute and relative paths. For instance:
``` sh
--path=C:\Users\...\model.tx
--path=./model.tx
```
- If you omit the `--full` flag, the CLI outputs only the raw regex by default. In contrast, when the flag is used, the full output is generated in a standalone file.
5. Run help:

i. Using narex command:
``` sh
narex
```
ii. Using help flag:
``` sh
narex --help
```

### VSCode extension
Prerequsities:
- Python VSCode extension (don't care now, it will be prompted if missing).

1. If you want to play with the extension, open the `extension` subproject in VSCode and run the following command:
``` sh
npm install
```
NOTE: Don't forget to activate the root project `.venv` from the subproject directory. If something goes wrong use `CTRL` + `SHIFT` + `P` -> `Select intepreter: ...` and select `python.exe` from the `.venv/Scripts` directory (_very importantly_).

2. Click on the `F5` key in Windows to start extension debugging.

3. Packaging is possible by running the following:
``` sh
vsce package
```
4. After packaging, the extension's `.vsix` file will be available. Install the extension by choosing the option `Install from vsix`. 
![alt text](image.png)
NOTE: Don't move the extension `.vsix` file out of the the extension directory before installation, as it is relatively positioned. If something goes bad, then very likely dependencies cause the headaches, thus go back to step 1.

### Automatic releasing
You can automatically trigger the release process by pushing a tag that starts with the letter `v`. For instance, `v1.2.3`.
1. Make sure to pull the changes before tagging:
``` sh 
git pull
```
2. Create a new tag:
``` sh
git tag <tag-name>
```
3. Push the tag to the remote repository:
``` sh
git push origin <tag-name>
```

### Static analysis
You can do it on your own.

Run the static analysis locally:
``` sh
mypy --strict <file-name>
```
Caveat: Static analysis is triggered automatically by GitHub Actions; therefore, it is smart to run a type checker from time to time before creating a pull request.


## References:
[1] [Source of the famous “Now you have two problems” quote](https://regex.info/blog/2006-09-15/247) _(Author: Jeffrey Friedl, Accessed: _July 19, 2025_)_