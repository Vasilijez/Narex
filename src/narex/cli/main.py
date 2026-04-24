import click
from click import group
from narex import get_metamodel, get_path
from narex.generators.python import PythonEngine

@click.group()
def cli():
    pass

def load_metamodel_and_model_path(path):
    mm = get_metamodel()
    p = get_path(path, False)
    m = mm.model_from_file(p)
    return mm, m

def load_metamodel_and_model_str(str):
    mm = get_metamodel()
    m = mm.model_from_str(str)
    return mm, m

@click.command()
@click.option('--path', default='', help='Enter path to model file')
def run_command(path):
    try:
        mm, m = load_metamodel_and_model_path(path)
        e = PythonEngine()
        result = e.generate(m)
        print(f"Result {result}")
    except Exception as e:
        print(f"An error occured while running the model: \n{e}")


@click.command()
@click.option('--path', default='', help='Enter path to model file')
def validate_command(path):
    try:
        _, m = load_metamodel_and_model_path(path)
        # validate(m)   # useless for now
    except Exception as e:
        print(f"An error occured while validating the model: \n{e}")


cli.add_command(validate_command)
cli.add_command(run_command)

if __name__ == '__main__':
    cli()