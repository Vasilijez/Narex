import re
import logging
from datetime import datetime
from lsprotocol import types
from pygls.lsp.server import LanguageServer
from textx import metamodel_from_file, TextXSyntaxError, TextXSemanticError
from narex import GRAMMAR_PATH

DATE_FORMATS = [
    "%H:%M:%S",
    "%d/%m/%y",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
]

class NarexLanguageServer(LanguageServer):
    def __init__(self, name, version, text_document_sync_kind = types.TextDocumentSyncKind.Incremental, notebook_document_sync = None, *args, **kwargs):
        super().__init__(name, version, text_document_sync_kind, notebook_document_sync, *args, **kwargs)
        self.mm = metamodel_from_file(GRAMMAR_PATH)

server = NarexLanguageServer("narex-server", "v1")


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def grammar_check(ls: NarexLanguageServer, params):

    ### Processing the grammar rules validation ###

    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)
    content = document.source
    diagnostics = []

    try:
        ls.mm.model_from_str(content)
    except (TextXSyntaxError, TextXSemanticError) as e:
        d = types.Diagnostic(
            range=types.Range(
                start=types.Position(line=e.line-1, character=e.col-1),
                end=types.Position(line=e.line-1, character=e.col)
            ),
            message=e.message,
            source="textX"
        )
        diagnostics.append(d)

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document_uri,
            diagnostics=diagnostics
        )
    )
    

def print_msg(ls: NarexLanguageServer, message):
    msg = ls.window_log_message(types.ShowMessageParams(
                message=message,
                type=types.MessageType.Info,
            ))
    return msg

def catch_current_word(content: str) -> str:
    match = re.search(r'(\w+)$', content)
    word = match.group(1).lower() if match else ""
    return word

def slice_document_after_cursor(document, params) -> str:
    offset = document.offset_at_position(params.position)
    content = document.source[:offset]
    return content

def is_eligble_keyword(label, eligble_keywords):
    if label in eligble_keywords:
        return True
    return False

def get_label(ls, rule, eligble_keywords) -> str | None:

    if hasattr(rule, 'to_match'):
        if is_eligble_keyword(rule.to_match, eligble_keywords):
            return rule.to_match
    
    elif hasattr(rule, 'rule_name'):
        # TODO: Which case???
        label = rule.rule_name.lower() if type(rule.rule_name) == "str" else rule.rule_name
        if is_eligble_keyword(label, eligble_keywords):
            return label
    
    elif hasattr(rule, 'name'):
        label = rule.name
        if is_eligble_keyword(label, eligble_keywords):
            return label

    return None

def sort_by_starts_with(params, current_word, label) -> types.CompletionItem:
    sort_priority = "0" if label.startswith(current_word) else "1"
    current_pos = params.position
    item = types.CompletionItem(
        label=label,
        kind=types.CompletionItemKind.Keyword,
        filter_text=current_word,
        sort_text=f"{sort_priority}"
    )

    return item 

def preselect_first_item(items: list[types.CompletionItem]):
    if len(items) >= 1:
        first_item = items[0]
        first_item.preselect = True

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def code_completion(ls: NarexLanguageServer, params):

    ### Based on the textX parser prediction it offers the completion rules ###
 
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)
    items = []

    # Cut off document content after cursor
    document = slice_document_after_cursor(document, params)

    # Catch current word
    current_word = catch_current_word(document)

    illegal_rules = {
        'UnescapedString', 'ID', 'EdgeValue'
    }

    eligble_keywords = {k.lower() for k in ls.mm.namespaces['narex'].keys() if k.lower() not in illegal_rules}

    try:
        ls.mm.model_from_str(document)


    except TextXSyntaxError as e:

        for rule in e.expected_rules:
            label = get_label(ls, rule, eligble_keywords)

            if label:
                item = sort_by_starts_with(params, current_word, label)
                
                # Put one of the top priorty elements at the first position
                # Do that as preparation for preselect
                if item.sort_text.startswith("0"):
                    items.insert(0, item)
                
                items.append(item)

    except (TextXSemanticError, Exception) as e:
        print_msg(ls, str(e))
        pass

    return types.CompletionList(is_incomplete=False, items=items) # maybe True


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
