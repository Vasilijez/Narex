"""
This is a variant of calc example using object processors for on-the-fly
evaluation.
"""
from textx import metamodel_from_file                       
from textx.export import metamodel_export, model_export     
from os.path import dirname, join

# def literal_action(literal: any) -> any:
#     ret = literal.value
#     return ret

def main(debug: bool = False) -> None:

    this_folder = dirname(__file__)

    var = 1

    # Get meta-model from language description
    mm = metamodel_from_file(join(this_folder, 'grammar.tx'), auto_init_attributes=False, debug=debug)
    # Instantiate model
    m = mm.model_from_file(join(this_folder, 'input.nx'))

    result = m.value

    # Optionally export model or metamodel to dot
    if debug:
        metamodel_export(mm, join(this_folder, 'visualization/metamodel.dot'))
        model_export(m, join(this_folder, 'visualization/model.dot'))
    assert result == "example"

if __name__ == '__main__':
    main()
