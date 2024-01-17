"""This module contains dataclasses relating to KMD Nova cases."""

from datetime import date
from dataclasses import dataclass

# All classes in this module are pure dataclasses made to contain data.
# pylint: disable=too-many-instance-attributes


@dataclass
class CaseParty:
    """A dataclass representing a case party in a KMD Nova case."""
    identification_type: str
    identification: str
    role: str
    name: str


@dataclass
class NovaDocument:
    """A dataclass representing af KMD Nova Document."""
    uuid: str
    title: str
    sensitivity: str
    document_type: str
    description: str
    approved: bool
    document_date: date
    file_extension: str


@dataclass
class NovaCase:
    """A dataclass representing a KMD Nova case."""
    uuid: str
    title: str
    case_number: str
    case_date: date
    active_code: str
    progress_state: str
    case_parties: list[CaseParty]
    documents: list[NovaDocument]
