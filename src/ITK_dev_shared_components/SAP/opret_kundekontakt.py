import win32clipboard

def opret_kundekontakter(session, fp, aftaler, art, notat, lock=None):
    session.StartTransaction('fmcacov')

    # Find forretningspartner
    session.findById("wnd[0]/usr/ctxtGPART_DYN").text = fp
    session.findById("wnd[0]").sendVKey(0)

    # Klik 'Opret kundekontakt-flere
    session.findById("wnd[0]/shellcont/shell").nodeContextMenu("GP0000000001")
    session.findById("wnd[0]/shellcont/shell").selectContextMenuItem("FLERE")

    # Vælg aftaler
    tree = session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[1]")
    # TODO: Vælg aftaler
    session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[0]").pressButton("OK")

    #Set art
    session.findById("wnd[0]/usr/tabsTSTRIP/tabpT_CA/ssubSUBSR_TSTRIP:SAPLBPT1:0510/cmbBCONTD-CTYPE").Value = art

    #Go to editor and paste
    session.findById("wnd[0]/usr/subNOTICE:SAPLEENO:1002/btnEENO_TEXTE-EDITOR").press()
    if lock: lock.acquire()
    setClipboard(notat)
    session.findById("wnd[0]/tbar[1]/btn[9]").press()
    if lock: lock.release()

    # Back and save
    session.findById("wnd[0]/tbar[0]/btn[3]").press()
    session.findById("wnd[0]/tbar[0]/btn[11]").press()

def setClipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()