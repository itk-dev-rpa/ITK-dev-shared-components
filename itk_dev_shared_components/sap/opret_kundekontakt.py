"""This module provides a single function to conveniently perform the action 'opret-kundekontaker' in SAP."""

from typing import Literal
from datetime import date

import win32clipboard

from itk_dev_shared_components.sap import tree_util, fmcacov


def opret_kundekontakter(session, fp: str, aftaler: list[str] | None,
                         art: Literal[' ', 'Automatisk', 'Fakturagrundlag', 'Fuldmagt ifm. værge', 'Konverteret', 'Myndighedshenvend.', 'Orientering', 'Returpost', 'Ringeaktivitet', 'Skriftlig henvend.', 'Telefonisk henvend.'],
                         notat: str, lock=None) -> None:
    """Creates a kundekontakt on the given FP and aftaler.

    Args:
        session: The SAP session to preform the action.
        fp: The forretningspartner number.
        aftaler: A list of aftaler to put the kundekontakt on. If empty or None the kundekontakt will be created on fp-level.
        art: The art of the kundekontakt.
        notat: The text of the kundekontakt.
        lock: A threading.Lock object to allow this function to run properly when multithreaded. Defaults to None.

    Raises:
        RuntimeError: If the kundekontakt wasn't created.
    """
    fmcacov.open_forretningspartner(session, fp)

    # Click 'Opret kundekontakt-flere
    session.findById("wnd[0]/shellcont/shell").nodeContextMenu("GP0000000001")
    session.findById("wnd[0]/shellcont/shell").selectContextMenuItem("FLERE")

    # When running multithreaded the toolbar buttons in the pop-up doesn't appear sometimes.
    # Open and close the pop-up until they appear
    for _ in range(10):
        if session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[0]").ButtonCount == 2:
            break
        session.findById("wnd[1]").close()
        session.findById("wnd[0]/shellcont/shell").nodeContextMenu("GP0000000001")
        session.findById("wnd[0]/shellcont/shell").selectContextMenuItem("FLERE")
    else:
        raise RuntimeError("The toolbar buttons in 'Opret kundekontakter-flere' didn't show up after 10 tries.")

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

    _confirm_kundekontakt(session, notat, art)


def _set_clipboard(text: str) -> None:
    """Private function to set text to the clipboard.

    Args:
        text: Text to set to clipboard.
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()


def _confirm_kundekontakt(session, notat: str, art: str):
    """Confirm the kundekontakt was created
    Compare the top 10 kundekontakter in the table with the input of this function
    Compare date, art and (up to) the first 10 letters of the notat
    """
    session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC3").select()
    table = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC3/ssubDATA_DISP_SCA:RFMCA_COV:0204/cntlRFMCA_COV_0100_CONT3/shellcont/shell")

    rows = min(10, table.RowCount)

    for row in range(rows):
        kundekontakt_date = table.GetCellValue(row, "DATE")
        kontaktart = table.GetCellValue(row, "ZZ_KONTAKTART")
        kontakttekst = table.GetCellValue(row, "ZZ_TEXT")

        length_to_compare = min([10, len(notat), len(kontakttekst)])

        if (date.today().strftime("%d.%m.%Y") == kundekontakt_date and art == kontaktart and notat[:length_to_compare] == kontakttekst[:length_to_compare]):
            break
    else:
        raise RuntimeError("The kundekontakt wasn't found in the kontakt-table after creation.")
