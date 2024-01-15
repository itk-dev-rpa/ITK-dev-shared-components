"""This module contains dataclasses relating to KMD Nova cases."""

from datetime import date
from dataclasses import dataclass


@dataclass
class CaseParty:
    """A dataclass representing a case party in a KMD Nova case."""
    identification_type: str
    identification: str
    role: str
    name: str


@dataclass
class NovaCase:
    """A dataclass representing a KMD Nova case."""
    uuid: str
    title: str
    case_number: str
    case_date: date
    case_parties: list[CaseParty]
