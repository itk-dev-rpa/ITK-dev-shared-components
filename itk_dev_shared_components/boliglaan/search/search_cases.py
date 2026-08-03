"""This module contains functions to search for cases
and handling the cases search results.
"""

from dataclasses import dataclass
from typing import Literal

from itk_dev_shared_components.boliglaan import common


CaseState = Literal[
    "Afslået",
    "Afventer bevilling",
    "Bevilget",
    "Udbetalt",
    "Afvikling - frivillig",
    "Afvikling - misligholdt afdrag kautionslån",
    "Afvikling - misligholdt kautionslån",
    "Afvikling - 5 års løbetid",
    "Afvikling - overskridelse af indkomstgrænse",
    "Afvikling - fraflyttet",
    "Afvikling - rentefri",
    "Gældssaneret",
    "Afskrevet - gældssaneret",
    "Afskrevet - lån uerholdeligt",
    "Afskrevet - dødsfald",
    "Afskrevet - RIM (Restance Inddrivelses Myndighed)",
    "Overført til anden person",
    "Overført/Annulleret",
    "Tilbageført",
    "Indfriet",
    "Annulleret lån",
    "Annulleret ansøgning"
]


CaseType = Literal[
    "Pligtlån 5 års løbetid §56, §57",
    "Pligtlån sanering §54",
    "Pligtlån pensionister §54",
    "Pligtlån enkeltværelse §54",
    "Pligtlån genhusning §54",
    "Pligtlån ældrebolig §54",
    "Flygtningelån 100% 5 års løbetid §66, §67",
    "Flygtningelån 100% sanering §66, §67",
    "Flygtningelån 100% pensionister §66, §67",
    "Flygtninglån 50% 5 års løbetid §68",
    "Kautionslån kaution §59",
    "Kautionslån flygtninge §68",
    "Kommune lån §59",
    "Garanti for istandsættelse"
]


@dataclass
class Case:
    """A dataclass representing a case from the case search result."""
    case_number: str
    cpr: str
    person_name: str
    address: str
    case_type: str
    case_state: str


def search_cases(cpr: str | None = None, street: str | None = None, types: tuple[CaseType] | None = None, states: tuple[CaseState] | None = None):
    """Search for cases.

    Args:
        cpr: The CPR number to look for.
        street: The street name to look for.
        types: The case types to look for.
        states: The case states to look for.
    """
    boliglaan = common.get_boliglaan()
    boliglaan.SendKeys("{Ctrl}B")

    popup = boliglaan.WindowControl(Name="Udsøg lånesager", searchDepth=1)

    if cpr:
        popup.TextControl(Name="Personnummer:").GetNextSiblingControl().GetValuePattern().SetValue(cpr)

    if street:
        popup.EditControl(AutomationId="vejSearchEdit").EditControl().GetValuePattern().SetValue(street)

    group = popup.GroupControl(Name="Lånetype", searchDepth=3)
    if types is None:
        group.CheckBoxControl(Name='Alle valgt').GetTogglePattern().SetToggleState(1)
    else:
        group.CheckBoxControl(Name='Alle valgt').GetTogglePattern().SetToggleState(0)

        for type_ in types:
            group.CheckBoxControl(Name=type_).GetTogglePattern().SetToggleState(1, waitTime=0)

    group = popup.GroupControl(Name="Lånestatus", searchDepth=3)
    if states is None:
        group.CheckBoxControl(Name='Alle valgt').GetTogglePattern().SetToggleState(1)
    else:
        group.CheckBoxControl(Name='Alle valgt').GetTogglePattern().SetToggleState(0)

        for state in states:
            group.CheckBoxControl(Name=state).GetTogglePattern().SetToggleState(1, waitTime=0)

    popup.ButtonControl(Name="Søg").Click(simulateMove=False)


def get_case_list() -> list[Case]:
    """Get the case search results as a list of Case objects."""
    boliglaan = common.get_boliglaan()

    grid = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).GroupControl(Name="Sager").DataGridControl(AutomationId="LaanesagerGridControl")
    grid_pattern = grid.GetGridPattern()

    result = []

    for row in range(grid_pattern.RowCount):
        new_case = Case(
            case_number=common.get_grid_value(grid_pattern, row, 0),
            cpr=common.get_grid_value(grid_pattern, row, 1),
            person_name=common.get_grid_value(grid_pattern, row, 2),
            case_state=common.get_grid_value(grid_pattern, row, 3),
            case_type=common.get_grid_value(grid_pattern, row, 4),
            address=common.get_grid_value(grid_pattern, row, 5)
        )

        result.append(new_case)

    return result


def select_case(cpr: str, case_number: str):
    """Select the case from the case search result with the given cpr and case number."""
    boliglaan = common.get_boliglaan()

    grid = boliglaan.TabControl(Name="TabbedGroup", searchDepth=4).GroupControl(Name="Sager").DataGridControl(AutomationId="LaanesagerGridControl")
    grid_pattern = grid.GetGridPattern()

    for row in range(grid_pattern.RowCount):
        row_case_number = common.get_grid_value(grid_pattern, row, 0)
        case_cpr = common.get_grid_value(grid_pattern, row, 1)

        if case_cpr == cpr and row_case_number == case_number:
            grid_pattern.GetItem(row, 0).DoubleClick(simulateMove=False)
            return

    raise LookupError(f"Couldn't find case: {cpr} - {case_number}")
