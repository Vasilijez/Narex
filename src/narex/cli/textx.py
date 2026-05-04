from narex import get_metamodel
from narex.cli.main import generate_with_print
from textx import generator, language
from textx.registration import GeneratorParam

@language('narex', '*.nx')
def textx_language():
    # TODO: Centralize description
    """
    Narex language
    """
    return get_metamodel()

@generator(
    'narex', 
    'python', 
    [GeneratorParam("cli-only", "Generate raw regex output to CLI only.", mandatory=False)]
)
def textx_python_generator(metamodel, model, output_path, overwrite, debug, **kwargs):
    full = kwargs.get('cli-only', False)
    generate_with_print(metamodel, model, output_path, overwrite, debug, full, 'python', 'textx')