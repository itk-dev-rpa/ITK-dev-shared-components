"""This module contains dataclasses relating to KMD Nova cases."""

from dataclasses import dataclass

# All classes in this module are pure dataclasses made to contain data.
# pylint: disable=too-many-instance-attributes


@dataclass(frozen=True, slots=True, kw_only=True)
class CaseParty:
    """A dataclass representing a case party in a KMD Nova case."""
    identification_type: str
    identification: str
    role: str
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Document:
    """A dataclass representing a KMD Nova Document."""
    uuid: str
    document_number: str
    title: str
    sensitivity: str
    document_type: str
    description: str
    approved: bool
    document_date: str
    file_extension: str


@dataclass(frozen=True, slots=True, kw_only=True)
class JournalNote:
    """A dataclass representing a KMD Nova journal note."""
    uuid: str
    title: str
    journal_date: str
    note_format: str
    note: bytes
    approved: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class NovaCase:
    """A dataclass representing a KMD Nova case."""
    uuid: str
    title: str
    case_number: str
    case_date: str
    active_code: str
    progress_state: str
    case_parties: list[CaseParty]
    document_count: int
    note_count: int
