import regex
import logging
from datetime import datetime
from lsprotocol import types
from pygls.lsp.server import LanguageServer
from textx import TextXSyntaxError, TextXSemanticError
from narex import get_metamodel
from typing import Any, List, Set
from pygls.workspace import TextDocument

DATE_FORMATS = [
    "%H:%M:%S",
    "%d/%m/%y",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
]

class NarexLanguageServer(LanguageServer):
    def __init__(
        self,
        name: str,
        version: str,
        text_document_sync_kind: types.TextDocumentSyncKind = types.TextDocumentSyncKind.Incremental,
        notebook_document_sync: types.NotebookDocumentSyncOptions | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, version, text_document_sync_kind, notebook_document_sync, *args, **kwargs)
        self.mm = get_metamodel()

server = NarexLanguageServer("narex-server", "v1")

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def grammar_check(ls: NarexLanguageServer, params: types.DidOpenTextDocumentParams | types.DidChangeTextDocumentParams) -> None:

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

def catch_current_word(ls: NarexLanguageServer, content: str) -> str:
    match = regex.search(r'(\w+)$', content)
    word = match.group(1).lower() if match else ""
    print_msg(ls, f"current_word {word}")
    return word

def slice_document_after_cursor(document: TextDocument, params: types.CompletionParams) -> str:
    offset = document.offset_at_position(params.position)
    content = document.source[:offset]
    return content

def is_eligble_keyword(label: str, eligble_keywords: Set[str]) -> bool:
    if label in eligble_keywords:
        return True
    return False
    
def get_label(rule: Any, eligble_keywords: Set[str]) -> str | None:

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

    if hasattr(rule, 'to_match'):
        # small_letter -> smallletter (rule in eligble_keywords)
        label = rule.to_match.replace("_", "")
        assert isinstance(rule.to_match, str)
        if is_eligble_keyword(label, eligble_keywords):
            return rule.to_match
    
    if hasattr(rule, 'name'):
        label = rule.name
        assert isinstance(label, str)
        if is_eligble_keyword(label, eligble_keywords):
            return label

    return None

def create_and_sort_by_starts_with(current_word: str, label: str) -> types.CompletionItem:
    sort_priority = "0" if label.startswith(current_word) else "1"

    item = types.CompletionItem(
        label=label,
        kind=types.CompletionItemKind.Keyword,
        filter_text=current_word,
        sort_text=f"{sort_priority}"
    )

    return item 

def is_id_rule(rule: Any) -> bool:
    return hasattr(rule, 'rule_name') and rule.rule_name == 'ID'

def get_offset_from_line_col(text: str, line: int, col: int) -> int:
    lines = text.splitlines(keepends=True)
    offset = sum(len(l) for l in lines[:line - 1]) + (col - 1)
    return offset

def get_ref_names(partial_model: str) -> List[str]:
    clause_refs_pat = r'[^\d\W]\w*\b(?=\s*{)'
    clause_refs: List[str] = regex.findall(pattern=clause_refs_pat, string=partial_model)

    group_refs_pat = r'group\s*\K[^\d\W]\w*\b(?=\s*of)'
    group_refs: List[str] = regex.findall(pattern=group_refs_pat, string=partial_model)

    return clause_refs + group_refs

def get_eligble_keywords(ls: NarexLanguageServer) -> Set[str]:
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
def code_completion(ls: NarexLanguageServer, params: types.CompletionParams) -> types.CompletionList:

    ### Based on the textX parser predicted rules are offered ###
 
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    # In order to avoid duplicates
    items = {}

    # Cut off document content after cursor
    document_text = slice_document_after_cursor(document, params)

    # Catch current word
    current_word = catch_current_word(ls, document_text)

    eligble_keywords = get_eligble_keywords(ls)

    try:
        ls.mm.model_from_str(document_text)

    except TextXSyntaxError as e:

        partial_offset = get_offset_from_line_col(document_text, e.line, e.col)
        partial_model = document_text[:partial_offset]
        ids = get_ref_names(partial_model)

        for rule in e.expected_rules:

            label = get_label(rule, eligble_keywords)

            if label:
                item = create_and_sort_by_starts_with(current_word, label)
                items[label] = item

            elif is_id_rule(rule):
                for label in ids:
                    item = create_and_sort_by_starts_with(current_word, label)
                    items[label] = item
        
    except (TextXSemanticError, Exception) as e:
        pass

    return types.CompletionList(is_incomplete=False, items=list(items.values())) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server.start_io()
