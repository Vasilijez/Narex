from textx import metamodel_from_file     
from os.path import dirname, join

def get_metamodel(debug=False):

    this_folder = dirname(__file__)
    grammar_path = join(this_folder, 'grammar', 'narex.tx')
    mm = metamodel_from_file(grammar_path, auto_init_attributes=False, debug=debug)

    return mm
