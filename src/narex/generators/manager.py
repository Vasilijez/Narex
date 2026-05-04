from narex.generators.python import PythonEngine
from narex.utils.loader import resolve_output_path, path_exists
from enum import Enum
from narex.utils.strings import normalize

ENGINES = {
    'python'
}

class GenStatus(Enum):
    SKIPPED = 1
    FULL = 2
    CLI_ONLY = 3

def generate(metamodel, model, output_path, overwrite, debug, cli_only, engine):

    match override_engine(parameter=engine, model=model):
        case 'python':
            e = PythonEngine()
            extension = 'py'
        case _:
            e = PythonEngine()
            extension = 'py'

    if cli_only == False:
        output_file_path = resolve_output_path(model, output_path, extension)

        if overwrite == False and path_exists(output_file_path):
            return GenStatus.SKIPPED, output_file_path, None
    else:
        output_file_path = ""
    
    result = e.generate(model=model, output_file_path=output_file_path, cli_only=cli_only)

    if cli_only:
        return GenStatus.CLI_ONLY, output_file_path, result
    else:
        return GenStatus.FULL, output_file_path, result

def override_engine(parameter: str | None, model: object) -> str:
    """
        Engine defined within the parameter overrides the parameter defined within the model.
    """
    parameter = normalize(parameter)

    if parameter in ENGINES:
        return parameter

    if is_engine_defined(model) and model.optional.engine.value in ENGINES:
        return model.optional.engine.value

    if parameter != "" or is_engine_defined(model):
        raise Exception("You can use only supported engines!")

    raise Exception("Engine must be defined either within the model or within the `--engine` flag!")

def is_engine_defined(model: object) -> bool:
    if model.optional and model.optional.engine:
        return True
    return False
