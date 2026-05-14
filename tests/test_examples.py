from narex import load_metamodel_and_model_str
from narex import PythonEngine

def test_characters() -> None:
    m = """
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"((one|two|three|[369])|[!.])"

def test_coefficients() -> None:
    m = """
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
        "x³ + x² + x + 1
        3x² - 125x + 12
        2x³ + 5x² + 8x - 15
        6x² + 18 - 35x
        12x³ + 95x² - 115"

        engine: 
            python

        target: 
            monomial
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\d{1,}(?=x²)"

def test_date() -> None:
    m = """
        day {
            digit between 0 and 3
            digit
        }

        month {
            either '0' or '1'
            digit
        }

        year {
            short_format {
                digit repeat 2 times
            }

            long_format {  
                digit repeat 4 times
            }

            either long_format or short_format
        }

        date {
            day
            '/'
            month
            '/'
            year
        }

        tests:
            "04/06/25",
            "18/12/05",
            "25/05/1998",
            "99/99/9999"

        target:
            date
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[0-3]\d\/(0|1)\d\/(\d{4}|\d{2})"

def test_email() -> None:
    m = """
      user {
            username {
            letter repeat 1 or more times
            }
            extended_username {
            '.' username 
            }

            username
            uncaptured group g1 {
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^[A-Za-z]{1,}(?:\.[A-Za-z]{1,}){0,}@[A-Za-z]{1,}(\.[A-Za-z]{1,}){1,}$"

def test_file() -> None:
    m = """
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\bfajl_v\d{0,}\.(png|pdf|jpeg)\b"

def test_phone_num() -> None:
    m = """
        carrier {
            digit repeat 2 times
        }

        state {
            '+'
            digit between 1 and 9
            digit repeat 2 to 3 times
        }

        no_state {
            '0'
        }

        separator {
            maybe either '/' or '-' or whitespace
        }

        local {
            digit repeat 3 times
            separator
            digit repeat 4 times
        }

        phone_number {
            starts
            either state or no_state
            separator
            carrier
            separator
            local
            ends
        }

        flags:
            global match,
            multiline

        engine:
            python

        tests:
            "+381 62 123 4567",
            "062/123-4567",
            "062-123-4567",
            "0621234567",
            "062 123 4567",
            "062.123.4567"

        target:
            phone_number 
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"^(\+[1-9]\d{2,3}|0)((\/|-|\s))?\d{2}((\/|-|\s))?\d{3}((\/|-|\s))?\d{4}$"

def test_positive_nums() -> None:
    m = """
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

      tests:
      "10 -25 -35 45
      -150 25 -35 -147
      8 -88 -888 -8888
      -3 -33 -333 -333"

      engine:
            python

      target:
            positive_number
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\b(?<!-)\d{1,}"

def test_price() -> None:
    m = """
        whole_value {
            digit between 1 and 9 repeat 1 or more times
            digit between 0 and 9 repeat 0 or more times
        }

        decimal_value {
            '.' digit repeat 1 or more times
        }

        price {
            '$'
            whole_value 
            maybe decimal_value
        }

        tests:
            "$3.45",
            "$23.32",
            "$400",
            "€3.44",
            "$.23"

        target:
            price
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\$[1-9]{1,}[0-9]{0,}(\.\d{1,})?"

def test_simple_number() -> None:
    m = """
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"[1-9]{1,}\d{0,}"

def test_repeated_numbers() -> None:
    m = """
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"(\d{1,})[A-Za-z]{1,}\1"