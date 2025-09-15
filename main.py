"""
This is a variant of calc example using object processors for on-the-fly
evaluation.
"""
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from os.path import dirname, join
def main(debug=False):

    this_folder = dirname(__file__)


    # Get meta-model from language description
    mm = metamodel_from_file(join(this_folder, 'grammar.tx'), auto_init_attributes=False, debug=debug)
    # Instantiate model
    m = mm.model_from_file(join(this_folder, 'input.nx'))
    # Optionally export model or metamodel to dot
    if debug:
        metamodel_export(mm, join(this_folder, 'visualization/metamodel.dot'))
        model_export(m, join(this_folder, 'visualization/model.dot'))
if __name__ == '__main__':
    main()
