import click
from narex import load_metamodel_and_model_path
from narex.cli.main import generate_with_print

@click.group()
def cli():
    pass

@click.command()
@click.option('--path', default='', help='Enter path of model file')
@click.option('--cli_only', is_flag=True, help='Generate raw regex output to CLI only')
@click.option('--output_path', is_flag=False, help='Enter path to output directory')
@click.option('--engine', default='python', help='Enter a regex engine')
@click.option('--overwrite', is_flag=True, help='Overwrite an existing output file')
@click.option('--debug', default='python', help='Debug command executing')
def run_command(path, cli_only, output_path, engine, overwrite, debug):
    try:
        mm, m = load_metamodel_and_model_path(file_path=path)
        generate_with_print(mm, m, output_path, overwrite, debug, cli_only, engine, cli="narex")

    except Exception as e:
        click.secho(click.style(f"An error occurred while validating the model: \n{e}", fg='red'))

@click.command()
@click.option('--path', default='', help='Enter path to model file')
def validate_command(path):
    try:
        _, m = load_metamodel_and_model_path(path)
        click.secho(click.style("Your model is correct!", fg='green'))
    except Exception as e:
        click.secho(click.style(f"An error occurred while validating the model: \n{e}", fg='red'))

cli.add_command(validate_command)
cli.add_command(run_command)

if __name__ == '__main__':
    cli()