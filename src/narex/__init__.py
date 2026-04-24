from textx import metamodel_from_file     
from os.path import dirname, join, abspath, pardir, isabs
from narex.validators.rules import validate_class_reference, validate_domain, validate_repeat, validate_literal

def get_metamodel(debug=False):

    this_folder = dirname(__file__)
    grammar_path = join(this_folder, 'grammar', 'narex.tx')
    mm = metamodel_from_file(grammar_path, auto_init_attributes=False, debug=debug)

    mm.register_model_processor(validate_class_reference)
    mm.register_obj_processors({
        'Domain': validate_domain,
        'Repeat': validate_repeat,
        'Literal': validate_literal
    })

    return mm

def get_path(path='', debug=False):
    """
        An absolute path is favored over relative path.
    """
    this_folder = dirname(__file__)


    if not path:
        this_folder = dirname(__file__)
        grammar_path = abspath(join(this_folder, pardir, pardir, 'examples', 'input.nx'))
    elif isabs(path):
        grammar_path = path
    else:
        grammar_path = abspath(path)
       
    if debug:
        print(f"Normalized path is {grammar_path}")
    
    return grammar_path