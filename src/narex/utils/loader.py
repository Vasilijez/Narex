from textx import metamodel_from_file
from os.path import dirname, join, abspath, pardir, isabs, exists, splitext, basename
from narex.validators.rules import validate_class_reference, validate_domain, validate_repeat, validate_literal

DEFAULT_INPUT_FILE_NAME = 'input.nx'
DEFAULT_INPUT_FILE_PATH = join(dirname(__file__), pardir, pardir, pardir, 'examples', DEFAULT_INPUT_FILE_NAME)
DEFAULT_GRAMMAR_PATH = join(dirname(__file__), '../grammar', 'narex.tx')

def load_metamodel_and_model_path(file_path):
    mm = get_metamodel()
    p = resolve_input_path(file_path, False)
    m = mm.model_from_file(p)
    return mm, m

def load_metamodel_and_model_str(str):
    mm = get_metamodel()
    m = mm.model_from_str(str)
    return mm, m


def get_metamodel(debug=False):

    grammar_path = DEFAULT_GRAMMAR_PATH
    mm = metamodel_from_file(grammar_path, auto_init_attributes=False, debug=debug)

    mm.register_model_processor(validate_class_reference)
    mm.register_obj_processors({
        'Domain': validate_domain,
        'Repeat': validate_repeat,
        'Literal': validate_literal
    })

    return mm

def resolve_input_path(path='', debug=False):
    """
        Given path will be validated and resolved. In contrary the default
        file path of input file will be used.

        Both path types can be used, either absolute or relative.
    """

    if not path:
        model_path = abspath(DEFAULT_INPUT_FILE_PATH)
    elif isabs(path):
        model_path = path
    else:
        model_path = abspath(path)

    if not path_exists(path):
        raise Exception("Input file path is not valid!")
       
    if debug:
        print(f"Normalized path is {model_path}")
    
    return model_path

def resolve_output_path(model, output_path=None, gen_extension='py'):
    """
        If the `output_path` is not provided, the new path will be created
        within the same directory where the `input_file` is located.
    """

    input_file = model._tx_filename
    output_dir = abspath(output_path if output_path else dirname(input_file))

    if not path_exists(output_dir):
        raise Exception("Input file path is not valid!")

    output_file_name = create_default_output_path(input_file, gen_extension)
    output_file_path = join(output_dir, output_file_name)

    return output_file_path

def create_default_output_path(input_file, gen_extension):
    """
        Copy the file name from the input file to output file
        and change the extension.
    """
    base_name, _ = splitext(basename(input_file))
    output_file_name = f"{base_name}.{gen_extension}"
    return output_file_name

def path_exists(path):
    return exists(path)