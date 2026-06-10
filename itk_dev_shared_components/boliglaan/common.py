"""This module contains functions to perform common actions in Boliglån."""

import time
from typing import Literal

import uiautomation
from uiautomation import PatternId


TabName = Literal["Låneoplysninger", "Advis", "Låneafvikling", "Dokumenter", "Dokumentunderskrifter", "Hændelser"]


def get_boliglaan() -> uiautomation.WindowControl:
    """Get the Boliglån main window."""
    return uiautomation.WindowControl(Name="KMD Boliglån", searchDepth=1)


def get_tab(tab_name: TabName) -> uiautomation.TabItemControl:
    """Get the tab with the given name."""
    bolig = get_boliglaan()
    tab_control = bolig.TabControl(AutomationId="DXTabControlTabControlMain", searchDepth=6)
    return tab_control.TabItemControl(Name=f"DXTabItem{tab_name}", searchDepth=1)


def select_tab(tab_name: TabName):
    """Select the tab with the given name."""
    get_tab(tab_name).GetSelectionItemPattern().Select()


def pin_sidebar():
    """Unfold the search side bar and pin it."""
    boliglaan = get_boliglaan()
    group = boliglaan.GroupControl(AutomationId="DockLayoutManager", searchDepth=2)

    pane = group.CustomControl(AutomationId="PART_LeftAutoHideTrayPanel")
    pane.GetPattern(PatternId.ExpandCollapsePattern).Expand()

    group.ButtonControl(AutomationId="PART_PinButton").GetInvokePattern().Invoke()


def wait_for_case_load(cpr: str, case_number: str, timeout: int = 15):
    """Wait for the case to load.

    Args:
        cpr: The cpr number of the case.
        case_number: The case number to wait for.
        timeout: The maximum number of seconds to wait. Defaults to 15.

    Raises:
        LookupError: If the cpr isn't loaded.
        LookupError: If the case number isn't loaded.
    """
    boliglaan = get_boliglaan()

    # Look for cpr
    info_box = boliglaan.CustomControl(ClassName="LaanTagerOplysningerUserControl", searchDepth=6)
    if not info_box.TextControl(RegexName=f"{cpr}.*", searchDepth=1).Exists(maxSearchSeconds=timeout):
        raise LookupError(f"Cpr wasn't found: {cpr}")

    # Look for case number
    loan_tab = get_tab("Låneoplysninger")
    loan_tab.GetSelectionItemPattern().Select()
    info_group = loan_tab.GroupControl(Name="Andre oplysninger", searchDepth=3)

    for _ in range(timeout):
        case_number_value = info_group.TextControl(Name="Sagsnummer:").GetNextSiblingControl().Name
        if case_number_value == case_number:
            break
        time.sleep(1)
    else:
        raise LookupError(f"Case number wasn't found: {case_number}")

    print(f"Case loaded {cpr}, {case_number}")
