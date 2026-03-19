
from narex import get_metamodel
from narex.generators.python import generate

def run():
    mm = get_metamodel()

    try:
        m = mm.model_from_file("examples/input.tx")
        result = generate(m)
        print(f"Result {result}")
    except Exception as e:
        print(f"Error {e}")

if __name__ == "__main__":
    run()