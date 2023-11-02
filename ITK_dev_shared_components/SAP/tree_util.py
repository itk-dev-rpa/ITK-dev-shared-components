"""This module provides static functions to peform common tasks with SAP GuiTree COM objects."""

def get_node_key_by_text(tree, text: str, fuzzy=False) -> str:
    """Get the node key of a node based on its text.
    tree: A SAP GuiTree object.
    text: The text to search for.
    fuzzy: Whether to check if the node text just contains the search text.
    """
    for key in tree.GetAllNodeKeys():
        t = tree.GetNodeTextByKey(key)

        if t == text or (fuzzy and text in t):
            return key
    
    raise ValueError(f"No node with the text '{text}' was found.")

def get_item_by_text(tree, text: str, fuzzy=False) -> tuple[str,str]:
    """Get the node key and item name of an item based on its text.
    tree: A SAP GuiTree object.
    text: The text to search for.
    fuzzy: Whether to check if the item text just contains the search text.
    """
    for key in tree.GetAllNodeKeys():
        for name in tree.GetColumnNames():
            t = tree.GetItemText(key, name)
            
            if t == text or (fuzzy and text in t):
                return (key, name)
    
    raise ValueError(f"No item with the text '{text}' was found.")

def check_all_check_boxes(tree) -> None:
    """Find and check all checkboxes in the tree.
    tree: A SAP GuiTree object.
    """
    for key in tree.GetAllNodeKeys():
        for name in tree.GetColumnNames():
            if tree.GetItemType(key, name) == 3:
                tree.ChangeCheckBox(key, name, True)

def uncheck_all_check_boxes(tree) -> None:
    """Find and uncheck all checkboxes in the tree.
    tree: A SAP GuiTree object.
    """
    for key in tree.GetAllNodeKeys():
        for name in tree.GetColumnNames():
            if tree.GetItemType(key, name) == 3:
                tree.ChangeCheckBox(key, name, False)




if __name__ == '__main__':
    from ITK_dev_shared_components.SAP import multi_session

    session = multi_session.spawn_sessions(1)[0]

    tree = session.findById('/app/con[0]/ses[0]/wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[1]')

    # print([tree.GetNodeTextByKey(key) for key in tree.GetAllNodeKeys()])
    # print([tree.GetItemText(key, '&Hierarchy') for key in tree.GetAllNodeKeys()])

    # print(list(tree.GetColumnNames()))

    # print(tree.GetItemText('          2', '&Hierarchy'))

    # key, name = get_item_by_text(tree, '2291987', True)
    # tree.ChangeCheckBox(key, name, True)

    check_all_check_boxes(tree)
    uncheck_all_check_boxes(tree)