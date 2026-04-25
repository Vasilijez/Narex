import click
from narex import load_metamodel_and_model_path
from narex.generators.python import PythonEngine

@click.group()
def cli():
    pass


@click.command()
@click.option('--path', default='', help='Enter path to model file')
@click.option('--full', is_flag=True, help='Generate full code to an output file')
def run_command(path, full):
    try:
        mm, m = load_metamodel_and_model_path(path)
        e = PythonEngine()
        result = e.generate(m, False) if full else e.generate(m)
        click.secho(click.style(f"Raw regex output: {result}", fg='green'))
        if full:
            click.secho(click.style(f"Full code generated and saved to: /src/narex/generators/out_regex.py", fg='blue'))
    except Exception as e:
        click.secho(click.style(f"An error occured while running the model: \n{e}", fg='red'))

@click.command()
@click.option('--path', default='', help='Enter path to model file')
def validate_command(path):
    try:
        _, m = load_metamodel_and_model_path(path)
        click.secho(click.style("Your model is correct!", fg='green'))
    except Exception as e:
        click.secho(click.style(f"An error occured while validating the model: \n{e}", fg='red'))


cli.add_command(validate_command)
cli.add_command(run_command)

if __name__ == '__main__':
    cli()