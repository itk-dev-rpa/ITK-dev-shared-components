"""This module contains functions to search for advis
and handling the advis search results.
"""

from dataclasses import dataclass
from datetime import date
from typing import Literal

from itk_dev_shared_components.boliglaan import common


AdvisType = Literal[
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
    case_type: str
    type: str
    state: str


def search_advis(cpr: str | None = None, date_from: date | None = None, date_to: date | None = None, types: tuple[AdvisType] | None = None):
    """Search for advis.

    Args:
        cpr: The cpr to look for.
        date_from: The date to search from.
        date_to: The date to search to.
        types: The types of advis to search for. If None all types are chosen.
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

    if types is None:
        popup.CheckBoxControl(Name='Vælg alle').GetTogglePattern().SetToggleState(1)
    else:
        popup.CheckBoxControl(Name='Vælg alle').GetTogglePattern().SetToggleState(0)

        for type_ in types:
            popup.CheckBoxControl(Name=type_).GetTogglePattern().SetToggleState(1, waitTime=0)

    popup.ButtonControl(Name="Søg").Click(simulateMove=False)


def select_advis(cpr: str, case_number: str):
    """Select the advis from the search list with the given cpr and case number."""
    boliglaan = common.get_boliglaan()
    grid = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).GroupControl(Name="Advis").DataGridControl(AutomationId="AdvisGridControl")
    grid_pattern = grid.GetGridPattern()

    for row in range(grid_pattern.RowCount):
        row_case_number = common.get_grid_value(grid_pattern, row, 1)
        case_cpr = common.get_grid_value(grid_pattern, row, 2)

        if case_cpr == cpr and row_case_number == case_number:
            grid_pattern.GetItem(row, 0).DoubleClick(simulateMove=False)
            return

    raise LookupError(f"Couldn't find advis: {cpr} - {case_number}")


def get_advis_list() -> list[Advis]:
    """Get the advis search result as a list of Advis objects."""
    boliglaan = common.get_boliglaan()

    grid = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).GroupControl(Name="Advis").DataGridControl(AutomationId="AdvisGridControl")
    grid_pattern = grid.GetGridPattern()

    result = []

    for row in range(grid_pattern.RowCount):
        date_str: str = common.get_grid_value(grid_pattern, row, 0)
        case_number = common.get_grid_value(grid_pattern, row, 1)
        cpr = common.get_grid_value(grid_pattern, row, 2)
        type_ = common.get_grid_value(grid_pattern, row, 3)
        state = common.get_grid_value(grid_pattern, row, 4)
        case_type = common.get_grid_value(grid_pattern, row, 6)

        day, month, year = (int(part) for part in date_str.split("-"))
        date_ = date(year, month, day)

        result.append(Advis(date=date_, cpr=cpr, case_number=case_number, type=type_, state=state, case_type=case_type))

    return result
