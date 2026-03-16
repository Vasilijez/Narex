import logging
from datetime import datetime
from lsprotocol import types
from pygls.lsp.server import LanguageServer
from textx import metamodel_from_file, TextXSyntaxError
import os


DATE_FORMATS = [
    "%H:%M:%S",
    "%d/%m/%y",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
]

current_dir = os.path.dirname(os.path.abspath(__file__))
grammar_path = os.path.join(current_dir, 'grammar.tx')

class NarexLanguageServer(LanguageServer):
    def __init__(self, name, version, text_document_sync_kind = types.TextDocumentSyncKind.Incremental, notebook_document_sync = None, *args, **kwargs):
        super().__init__(name, version, text_document_sync_kind, notebook_document_sync, *args, **kwargs)
        self.mm = metamodel_from_file(grammar_path)

server = NarexLanguageServer("narex-server", "v1")

@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: NarexLanguageServer, params: types.HoverParams):
    
    ### Used only for testing (learning) purposes ###
    ### 01/01/20
    
    pos = params.position
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    try:
        line = document.lines[pos.line]
    except IndexError:
        return None

    for fmt in DATE_FORMATS:
        try:
            value = datetime.strptime(line.strip(), fmt)
            break
        except ValueError:
            pass

    else:
        # No valid datetime found.
        return None

    hover_content = [
        f"# {value.strftime('%a %d %b %Y')}",
        "",
        "| Format | Value |",
        "|:-|-:|",
        *[f"| `{fmt}` | {value.strftime(fmt)} |" for fmt in DATE_FORMATS],
    ]

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value="\n".join(hover_content),
        ),
        range=types.Range(
            start=types.Position(line=pos.line, character=0),
            end=types.Position(line=pos.line + 1, character=0),
        ),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server.start_io()
