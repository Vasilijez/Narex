import click, os
from narex import load_metamodel_and_model_path, get_metamodel
from narex.generators.python import PythonEngine
from textx import generator, language
from textx.registration import GeneratorParam

@click.group()
def cli():
    pass

# TODO: both input and output paths if provided need to be validated
@click.command()
@click.option('--path', default='', help='Enter path of model file')
@click.option('--full', is_flag=True, help='Generate full code to an output file')
@click.option('--output_path', is_flag=False, help='Enter path to output directory')
@click.option('--engine', default='python', help='Enter a regex engine')
@click.option('--overwrite', is_flag=True, help='Overwrite an existing output file')
@click.option('--debug', default='python', help='Debug command executing')
def run_command(path, full, output_path, engine, overwrite, debug):
    try:
        mm, m = load_metamodel_and_model_path(path)
        match engine:
            case 'python':
                generate_python(mm, m, output_path, overwrite, debug, full)

    except Exception as e:
        click.secho(click.style(f"An error occurred while running the model: \n{e}", fg='red'))


def generate_python(metamodel, model, output_path, overwrite, debug, full):
    output_file_path, output_file_dir = prepare_file_path(model, output_path, 'py')

    path_exists = not os.path.exists(output_file_dir)
    if overwrite == False or path_exists:
        click.secho(click.style(f"-- Skipping: {output_file_path}", fg='red'))
        return

    e = PythonEngine()
    result = e.generate(model=model, output_file_path=output_file_path, full=full)

    if full:
        click.secho(click.style(f"Full code generated and saved to: {output_file_path}", fg='blue'))
    else:
        click.secho(click.style(f"Raw regex output: {result}", fg='green'))

@generator(
    'narex', 
    'python', 
    [GeneratorParam("full", "Generate full code to an output file")]
)
def textx_python_generator(metamodel, model, output_path, overwrite, debug, full=False):
    generate_python(metamodel, model, output_path, overwrite, debug, full)

@language('narex', '*.nx')
def textx_language():
    """
    Narex language
    """
    return get_metamodel()

# Refactor later on maybe something cant work
# Rethink about logic of validating paths
# Shift to utils
def prepare_file_path(model, output_path, gen_extension='py'):
    input_file = model._tx_filename
    file_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file_name = "{}.{}".format(base_name, gen_extension)
    file_dir_abs = os.path.abspath(file_dir)
    output_file_path = os.path.join(file_dir_abs, output_file_name)

    return output_file_path, file_dir_abs


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