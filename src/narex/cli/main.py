import click
from click import group
from narex import get_metamodel, get_path
from narex.generators.python import generate
from narex.validators.rules import validate

@click.group()
def cli():
    pass

def load_model(path):
    mm = get_metamodel()
    p = get_path(path, True)
    m = mm.model_from_file(p)
    return mm, m

@click.command()
@click.option('--path', default='', help='Enter path to model file')
def run(path):
    try:
        mm, m = load_model(path)
        result = generate(m)
        print(f"Result {result}")
    except Exception as e:
        print(f"An error occured while validating the model {e}")

@click.command()
@click.option('--path', default='', help='Enter path to model file')
def validate(path):
    try:
        _, m = load_model(path)
        # validate(m)
    except Exception as e:
        print(f"An error occured while validating the model {e}")


cli.add_command(validate)
cli.add_command(run)

if __name__ == '__main__':
    cli()