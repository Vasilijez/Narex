from narex import load_metamodel_and_model_str
from narex import PythonEngine

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

def test_task_10() -> None:
    m = """
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
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"\$[1-9]{0,}(\.\d{0,})?"

def test_task_12() -> None:
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

        target:
            match
    """

    mm, m = load_metamodel_and_model_str(m)
    e = PythonEngine()
    r = e.generate(m, cli_only=True)
    assert r == r"((one|two|three|[369])|[!.])"


