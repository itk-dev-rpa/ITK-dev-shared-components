"""This module contains functions to help with actions in the fmcacov transaction."""


def open_forretningspartner(session, fp: str) -> None:
    """Start the transaction FMCACOV and open the given forretningspartner.
    If the fp-number also matches a cvr-number the fp-number will be opened.

    Args:
        session: The SAP session to perform the action.
        fp: The forretningspartner number.

    Raises:
        ValueError: If the forretningspartner wasn't found.
    """
    session.StartTransaction('fmcacov')

    # Find forretningspartner
    session.findById("wnd[0]/usr/ctxtGPART_DYN").text = fp
    session.findById("wnd[0]").sendVKey(0)

    # Detect window "Forretningspartner * Entries"
    if session.findById('wnd[1]/usr', False) is not None:
        # Pop-up detected
        for row_id in range(3, 5):
            fp_row = session.FindById(f'wnd[1]/usr/lbl[103,{row_id}]')
            if fp_row.text == fp:
                fp_row.SetFocus()
                # Press 'Accept' button.
                session.FindById('wnd[1]/tbar[0]/btn[0]').press()
                break
        else:
            # Range exhausted
            raise ValueError(f"Forretningspartner '{fp}' was not found in pop-up.")


def dismiss_key_popup(session, fp: str = "25564617") -> None:
    """Once a day a popup appears asking to generate a new "afstemningsnøgle".
    This function forces it to appear and clicks "Ja" on it.
    This is done by pretending to do "Kontovedligehold" on the given forretningspartner.
    The function should start and end at the home screen.

    Args:
        session: The SAP session object.
        fp: The forretningspartner to used. Defaults to "25564617" a fictional person in AAK.

    Raises:
        RuntimeError: If a popup other than the expected ones appear.
    """
    open_forretningspartner(session, fp)

    # Right click the first row in the postliste and click "Kontovedligehold med filter"
    postliste = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC1/ssubDATA_DISP_SCA:RFMCA_COV:0202/cntlRFMCA_COV_0100_CONT5/shellcont/shell")
    postliste.setCurrentCell(0, "VTREF")
    postliste.contextMenu()
    postliste.selectContextMenuItem("ACC_MAINT_FILTER")

    # Check if the key popup appeared
    popup = session.findbyid("wnd[1]", False)
    if popup:
        if popup.text == "Kontrol af afstemningsnøgle":
            # Press "Ja"
            session.findbyid("wnd[1]/usr/btnSPOP-OPTION1").press()
        else:
            raise RuntimeError(f"Another popup is blocking: {popup.text}")

        # Check and dismiss confirmation dialog
        confirmation_text = session.findbyid("wnd[1]/usr/txtMESSTXT1").text
        if 'oprettet' in confirmation_text:
            session.findById("wnd[1]/tbar[0]/btn[0]").press()
        else:
            raise RuntimeError(f"Confirmation dialog wasn't as expected: {confirmation_text}.")

    # Go back to home screen (Afbryd x 3)
    session.findById("wnd[0]/tbar[0]/btn[12]").press()
    session.findById("wnd[0]/tbar[0]/btn[12]").press()
    session.findById("wnd[0]/tbar[0]/btn[12]").press()
