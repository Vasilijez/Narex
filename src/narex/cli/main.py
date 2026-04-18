import click
from click import group
from narex import get_metamodel, get_path
from narex.generators.python import PythonEngine
from narex.validators.rules import validate_class_reference, validate_domain, validate_repeat, validate_literal

@click.group()
def cli():
    pass


def load_model(path):
    mm = get_metamodel()
    mm.register_model_processor(validate_class_reference)
    mm.register_obj_processors({
        'Domain': validate_domain,
        'Repeat': validate_repeat,
        'Literal': validate_literal
    })
    p = get_path(path, False)
    m = mm.model_from_file(p)
    return mm, m


@click.command()
@click.option('--path', default='', help='Enter path to model file')
def run_command(path):
    try:
        mm, m = load_model(path)
        e = PythonEngine()
        result = e.generate(m)
        print(f"Result {result}")
    except Exception as e:
        print(f"An error occured while running the model: \n{e}")


@click.command()
@click.option('--path', default='', help='Enter path to model file')
def validate_command(path):
    try:
        _, m = load_model(path)
        # validate(m)   # useless for now
    except Exception as e:
        print(f"An error occured while validating the model: \n{e}")


cli.add_command(validate_command)
cli.add_command(run_command)

if __name__ == '__main__':
    cli()