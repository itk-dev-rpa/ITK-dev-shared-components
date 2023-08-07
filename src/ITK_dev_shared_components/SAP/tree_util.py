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
    fuzzy: Whether to check if the node text just contains the search text.
    """
    for key in tree.GetAllNodeKeys():
        for name in tree.GetColumnNames():
            t = tree.GetItemText(key, name)
            
            if t == text or (fuzzy and text in t):
                return (key, name)
    
    raise ValueError(f"No item with the text '{text}' was found.")




if __name__ == '__main__':
    import win32com.client
    import time

    SAP = win32com.client.GetObject("SAPGUI")
    app = SAP.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(0)

    tree = session.findById('/app/con[0]/ses[0]/wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[1]')

    # print([tree.GetNodeTextByKey(key) for key in tree.GetAllNodeKeys()])
    # print([tree.GetItemText(key, '&Hierarchy') for key in tree.GetAllNodeKeys()])

    # print(list(tree.GetColumnNames()))

    # print(tree.GetItemText('          2', '&Hierarchy'))

    key, name = get_item_by_text(tree, '2291987', True)
    tree.ChangeCheckBox(key, name, True)