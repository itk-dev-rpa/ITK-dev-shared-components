"""This module provides a single function to conveniently peform the action 'opret-kundekontaker' in SAP."""

from typing import Literal
import win32clipboard
from ITK_dev_shared_components.SAP import tree_util


def opret_kundekontakter(session, fp:str, aftaler:list[str] | None,
                         art:Literal[' ', 'Automatisk', 'Fakturagrundlag', 'Fuldmagt ifm. værge', 'Konverteret', 'Myndighedshenvend.', 'Orientering', 'Returpost', 'Ringeaktivitet', 'Skriftlig henvend.', 'Telefonisk henvend.'],
                         notat:str, lock=None) -> None:
    """Creates a kundekontakt on the given FP and aftaler.

    Args:
        session (COM Object): The SAP session to peform the action.
        fp (str): The forretningspartner number.
        aftaler (list[str] | None): A list of aftaler to put the kundekontakt on. If empty or None the kundekontakt will be created on fp-level.
        art (str): The art of the kundekontakt.
        notat (str): The text of the kundekontakt.
        lock (threading.Lock, optional): A threading.Lock object to allow this function to run properly when multithreaded. Defaults to None.
    """
    session.StartTransaction('fmcacov')

    # Find forretningspartner
    session.findById("wnd[0]/usr/ctxtGPART_DYN").text = fp
    session.findById("wnd[0]").sendVKey(0)

    # Click 'Opret kundekontakt-flere
    session.findById("wnd[0]/shellcont/shell").nodeContextMenu("GP0000000001")
    session.findById("wnd[0]/shellcont/shell").selectContextMenuItem("FLERE")

    # Vælg aftaler
    if aftaler:
        aftale_tree = session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[1]")
        for aftale in aftaler:
            key, name = tree_util.get_item_by_text(aftale_tree, aftale, True)
            aftale_tree.ChangeCheckBox(key, name, True)
    session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[0]").pressButton("OK")

    # Set art
    session.findById("wnd[0]/usr/tabsTSTRIP/tabpT_CA/ssubSUBSR_TSTRIP:SAPLBPT1:0510/cmbBCONTD-CTYPE").Value = art

    # Go to editor and paste (lock if multithreaded)
    session.findById("wnd[0]/usr/subNOTICE:SAPLEENO:1002/btnEENO_TEXTE-EDITOR").press()
    if lock:
        lock.acquire()
    _set_clipboard(notat)
    session.findById("wnd[0]/tbar[1]/btn[9]").press()
    if lock:
        lock.release()

    # Back and save
    session.findById("wnd[0]/tbar[0]/btn[3]").press()
    session.findById("wnd[0]/tbar[0]/btn[11]").press()


def _set_clipboard(text:str) -> None:
    """Private function to set text to the clipboard.

    Args:
        text: Text to set to clipboard.
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
