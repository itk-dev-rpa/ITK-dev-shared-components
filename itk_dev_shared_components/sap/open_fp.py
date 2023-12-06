"""Method for opening Forretnignspartneroversigt in SAP"""


def find_forretningspartner(session, fp) -> None:
    """Start a transaction FMCACOV and open the fp. Dismiss pop-up where user must select CPR or CVR.
    The process will open Forretningspartneroversigt for the given fp.
    If the fp is invalid

    Args:
        session: The SAP session to preform the action.
        fp: The forretningspartner number.

    Raises:
        ValueError: If the forretningspartner was not found.
    """
    session.StartTransaction('fmcacov')

    # Find forretningspartner
    session.findById("wnd[0]/usr/ctxtGPART_DYN").text = fp
    session.findById("wnd[0]").sendVKey(0)
    # detect window "Forretningspartner * Entries"

    if session.findById('wnd[1]/usr', False) is not None:
        # pop-up detected
        for row_id in range(3, 5):
            fp_row = session.FindById(f'wnd[1]/usr/lbl[103,{row_id}]')
            if fp_row.text == fp:
                fp_row.SetFocus()
                # press 'Accept' button.
                session.FindById('wnd[1]/tbar[0]/btn[0]').press()
                break
        else:
            # range exhausted
            raise ValueError(f"ForretnPartner '{fp}' was not found in pop-up.")
