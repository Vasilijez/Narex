import regex
import logging
from datetime import datetime
from lsprotocol import types
from pygls.lsp.server import LanguageServer
from textx import TextXSyntaxError, TextXSemanticError
from narex import get_metamodel

DATE_FORMATS = [
    "%H:%M:%S",
    "%d/%m/%y",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
]

class NarexLanguageServer(LanguageServer):
    def __init__(self, name, version, text_document_sync_kind = types.TextDocumentSyncKind.Incremental, notebook_document_sync = None, *args, **kwargs):
        super().__init__(name, version, text_document_sync_kind, notebook_document_sync, *args, **kwargs)
        self.mm = get_metamodel()

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
    
def print_msg(ls: NarexLanguageServer, message: str) -> None:
    # Useful utility function.
    ls.window_log_message(types.LogMessageParams(
        type=types.MessageType.Info,
        message=message,
    ))

def catch_current_word(ls, content: str) -> str:
    match = regex.search(r'(\w+)$', content)
    word = match.group(1).lower() if match else ""
    print_msg(ls, f"current_word {word}")
    return word

def slice_document_after_cursor(document, params) -> str:
    offset = document.offset_at_position(params.position)
    content = document.source[:offset]
    return content

def is_eligble_keyword(label, eligble_keywords):
    if label in eligble_keywords:
        return True
    return False

def extract_ref_names(refs):
    names = []
    for r in refs:
        names.append(r.name)
    
def get_label(ls, rule, eligble_keywords) -> str | None:

    #
    #  rule                to_match                   rule_name                   name
    #
    #  \n                     \n                         sep                   StrMatch(\n)
    #  }                       }                       missing                 StrMatch(})
    #  ID                  [^\d\W]\w*\b                  ID                 ID=RegExMatch([^\d\W]\w*\b)
    #  UnescapedString  ("(?:[^"])*"|'(?:[^'])*')    UnescapedString  UnescapedString=RegExMatch(("(?:[^"])*"|'(?:[^'])*'))
    #  backreference       backreference                missing           StrMatch(backreference)
    #  Uncaptured          uncaptured                  Uncaptured          Uncaptured=StrMatch(uncaptured)
    #  lookahead           lookahead                    missing              StrMatch(lookahead)       
    #    
    #  either is like lookahead
    #  lookbehind is like lookahead
    #
    #  ends is like Uncaptured
    #  starts is like Uncaptured
    #  letter is like Uncaptured
    #  Negative is like Uncaptured
    #
    #  ...
    #

    r = rule
    if hasattr(rule, 'to_match'):
        # small_letter -> smallletter (rule in eligble_keywords)
        label = rule.to_match.replace("_", "")
        if is_eligble_keyword(label, eligble_keywords):
            return rule.to_match
    
    # if hasattr(rule, 'rule_name'):
    #     label = rule.rule_name.lower() if type(rule.rule_name) == "str" else rule.rule_name
    #     if is_eligble_keyword(label, eligble_keywords):
    #         return label
    
    if hasattr(rule, 'name'):
        label = rule.name
        if is_eligble_keyword(label, eligble_keywords):
            return label

    return None

def create_and_sort_by_starts_with(params, current_word, label) -> types.CompletionItem:
    sort_priority = "0" if label.startswith(current_word) else "1"

    item = types.CompletionItem(
        label=label,
        kind=types.CompletionItemKind.Keyword,
        filter_text=current_word,
        sort_text=f"{sort_priority}"
    )

    return item 

def is_id_rule(rule) -> bool:
    return hasattr(rule, 'rule_name') and rule.rule_name == 'ID'

def get_offset_from_line_col(text, line, col):
    lines = text.splitlines(keepends=True)
    offset = sum(len(l) for l in lines[:line - 1]) + (col - 1)
    return offset

def get_ref_names(partial_model) -> list[str]:
    clause_refs = r'[^\d\W]\w*\b(?=\s*{)'
    clause_refs = regex.findall(pattern=clause_refs, string=partial_model)

    group_refs = r'group\s*\K[^\d\W]\w*\b(?=\s*of)'
    group_refs = regex.findall(pattern=group_refs, string=partial_model)

    return clause_refs + group_refs

def get_eligble_keywords(ls) -> list[str]:
    illegal_rules = {
        'UnescapedString', 
        'EdgeValue', 
        'OneOf'     # Used eventually
        'ID',       # Used eventually
        'GlobalMatch',
        'CaseInsensitive',
        'SingleLine',
    }

    # Keywords of narex rules
    eligble_keywords = {k.lower() for k in ls.mm.namespaces['narex'].keys() if k.lower() not in illegal_rules}
    # Keywords defined within the rules
    # eligble_keywords.add('{')
    # eligble_keywords.add('}')
    # eligble_keywords.add(':')
    eligble_keywords.add('one')
    eligble_keywords.add('of')
    eligble_keywords.add('or')
    eligble_keywords.add('to')
    eligble_keywords.add('and')
    eligble_keywords.add('more')
    eligble_keywords.add('times')
    eligble_keywords.add('case')
    eligble_keywords.add('sensitive')
    eligble_keywords.add('global')
    eligble_keywords.add('match')
    eligble_keywords.add('single')
    eligble_keywords.add('line')

    return eligble_keywords

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def code_completion(ls: NarexLanguageServer, params):

    ### Based on the textX parser predicted rules are offered ###
 
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    # In order to avoid duplicates
    items = {}

    # Cut off document content after cursor
    document = slice_document_after_cursor(document, params)

    # Catch current word
    current_word = catch_current_word(ls, document)

    eligble_keywords = get_eligble_keywords(ls)

    try:
        m = ls.mm.model_from_str(document)

    except TextXSyntaxError as e:

        partial_offset = get_offset_from_line_col(document, e.line, e.col)
        partial_model = document[:partial_offset]
        ids = get_ref_names(partial_model)

        for rule in e.expected_rules:

            label = get_label(ls, rule, eligble_keywords)

            if label:
                item = create_and_sort_by_starts_with(params, current_word, label)
                items[label] = item

            elif is_id_rule(rule):
                for label in ids:
                    item = create_and_sort_by_starts_with(params, current_word, label)
                    items[label] = item
        
    except (TextXSemanticError, Exception) as e:
        pass

    return types.CompletionList(is_incomplete=False, items=items.values()) 


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
