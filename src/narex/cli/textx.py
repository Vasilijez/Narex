from narex import get_metamodel
from narex.cli.main import generate_with_print
from textx import generator, language
from textx.registration import GeneratorParam
from textx.metamodel import TextXMetaModel
from typing import Any

@language('narex', '*.nx')
def textx_language() -> TextXMetaModel:
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
def textx_python_generator(
        metamodel: TextXMetaModel, 
        model: Any, 
        output_path: str | None, 
        overwrite: bool = False, 
        debug: bool = False,
        **kwargs: Any
    ) -> None:

    cli_only = kwargs.get('cli-only', False)
    generate_with_print(metamodel, model, output_path, overwrite, debug, cli_only, 'python')