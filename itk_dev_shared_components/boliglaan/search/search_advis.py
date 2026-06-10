"""This module contains functions to search for advis
and handling the advis search results.
"""

from dataclasses import dataclass
from datetime import date
from typing import Literal

import uiautomation

from itk_dev_shared_components.boliglaan import common


AdvisType = Literal[
    'All',
    'Eget oprettet advis',
    'Indbetaling mangler på lånet i KMD Boliglån',
    'Lånet er ikke pålignet',
    'Lånet har afstemningssaldo selvom restgæld er 0 kr.',
    'Lånet har status "Afvikling..."/Gældssaneret - ej pålignet',
    'Lånets saldo = 0 kr.',
    'Lånets saldo er negativ',
    'Rente og afdragsfrihed på 5 år udløber'
]


@dataclass
class Advis:
    """A dataclass representing an advis
    from the advis search result.
    """
    date: date
    cpr: str
    case_number: str
    type: str
    state: str


def search_advis(cpr: str | None = None, date_from: date | None = None, date_to: date | None = None, types: tuple[AdvisType] = ('All',)):
    """Search for advis.

    Args:
        cpr: The cpr to look for. Defaults to None.
        date_from: The date to search from. Defaults to None.
        date_to: The date to search to. Defaults to None.
        types: The types of advis to search for. Defaults to ['Vælg alle'].

    Raises:
        ValueError: If 'All' is not alone in the types list.
    """
    boliglaan = common.get_boliglaan()
    boliglaan.SendKeys("{Ctrl}T")

    popup = boliglaan.WindowControl(Name="Søg advis", searchDepth=1)

    if cpr:
        popup.TextControl(Name="Personnummer:").GetNextSiblingControl().GetValuePattern().SetValue(cpr)

    if date_from:
        popup.TextControl(Name="Dato fra:").GetNextSiblingControl().GetValuePattern().SetValue(date_from.strftime("%d-%m-%Y"))

    if date_to:
        popup.TextControl(Name="Dato til:").GetNextSiblingControl().GetValuePattern().SetValue(date_to.strftime("%d-%m-%Y"))

    if 'All' in types and len(types) != 1:
        raise ValueError("Can't have more than one type when 'All' is chosen")

    if 'All' in types:
        popup.CheckBoxControl(Name='Vælg alle').GetTogglePattern().SetToggleState(1)
    else:
        popup.CheckBoxControl(Name='Vælg alle').GetTogglePattern().SetToggleState(0)

        for type_ in types:
            popup.CheckBoxControl(Name=type_).GetTogglePattern().SetToggleState(1, waitTime=0)

    popup.ButtonControl(Name="Søg").GetInvokePattern().Invoke()


def select_advis(cpr: str, case_number: str):
    """Select the advis from the search list with the given cpr and case number."""
    boliglaan = common.get_boliglaan()
    rows = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).PaneControl(AutomationId="dataPresenter").GetChildren()

    for row in rows:
        row_case_number = row.CustomControl(foundIndex=2).GetPattern(uiautomation.PatternId.ValuePattern).Value
        case_cpr = row.CustomControl(foundIndex=3).GetPattern(uiautomation.PatternId.ValuePattern).Value

        if case_cpr == cpr and row_case_number == case_number:
            row.DoubleClick(simulateMove=False)
            return

    raise LookupError(f"Couldn't find advis: {cpr} - {case_number}")


def get_advis_list() -> list[Advis]:
    """Get the advis search result as a list of Advis objects."""
    boliglaan = common.get_boliglaan()
    rows = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).PaneControl(AutomationId="dataPresenter").GetChildren()

    result = []

    for row in rows:
        date_str: str = row.CustomControl(foundIndex=1).GetPattern(uiautomation.PatternId.ValuePattern).Value
        case_number = row.CustomControl(foundIndex=2).GetPattern(uiautomation.PatternId.ValuePattern).Value
        cpr = row.CustomControl(foundIndex=3).GetPattern(uiautomation.PatternId.ValuePattern).Value
        type_ = row.CustomControl(foundIndex=4).GetPattern(uiautomation.PatternId.ValuePattern).Value
        state = row.CustomControl(foundIndex=5).GetPattern(uiautomation.PatternId.ValuePattern).Value

        day, month, year = (int(part) for part in date_str.split("-"))
        date_ = date(year, month, day)

        result.append(Advis(date=date_, cpr=cpr, case_number=case_number, type=type_, state=state))

    return result
