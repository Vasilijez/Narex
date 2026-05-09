import click
from narex.generators.manager import GenStatus, generate
from textx.metamodel import TextXMetaModel
from typing import Any

def generate_with_print(
        metamodel: TextXMetaModel, 
        model: Any, 
        output_path: str | None, 
        overwrite: bool = False, 
        debug: bool = False,
        cli_only: bool = False, 
        engine: str | None = None
    ) -> None:
    
    try:
        status, output_file_path, result = generate(
            metamodel, 
            model, 
            output_path, 
            overwrite, 
            debug, 
            cli_only, 
            engine
        )

        match status:
            case GenStatus.SKIPPED:
                click.secho(click.style(f"Skipping since the overwrite flag is not passed: {output_file_path}", fg='red'))
            
            case GenStatus.FULL:
                click.secho(click.style(f"Full code generated and saved to: {output_file_path}", fg='blue'))
            
            case GenStatus.CLI_ONLY:
                click.secho(click.style(f"Raw regex output: {result}", fg='green'))

    except Exception as e:
        click.secho(click.style(f"An error occurred while running the model: \n{e}", fg='red'))

