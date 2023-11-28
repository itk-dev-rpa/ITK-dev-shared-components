"""This module provides miscellaneous static functions to perform common tasks in SAP."""


def print_all_descendants(container, max_depth=-1, indent=0):
    """Prints the object and all of its descendants recursively
    to the console.

    Args:
        container: A SAP GuiContainer object.
        max_depth: The maximum depth of the recursive search. Defaults to -1.
        indent: The indentation level of the printed text.
                This increases for each level of the recursion. Defaults to 0.
    """
    indent_text = '   |'*indent

    for child in container.Children:
        print(indent_text, child.Type)
        print(indent_text, child.Name)
        print(indent_text, child.Id)

        if (hasattr(child, 'Children') and child.Children is not None
                and len(child.Children) != 0
                and (indent < max_depth or max_depth == -1)):

            print_all_descendants(child, max_depth, indent+1)
        else:
            print(indent_text)
