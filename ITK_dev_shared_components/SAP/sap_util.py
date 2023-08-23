def print_all_descendants(container, max_depth=-1, indent=0):
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


if __name__=='__main__':
    import win32com.client

    SAP = win32com.client.GetObject("SAPGUI")
    app = SAP.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(0)

    usr = session.FindById('/app/con[0]/ses[0]/wnd[0]/usr')

    print_all_descendants(usr)