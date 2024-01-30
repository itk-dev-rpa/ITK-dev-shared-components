"""This module contains dataclasses relating to KMD Nova cases."""

from dataclasses import dataclass
from typing import Literal, Optional
from datetime import datetime

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
    title: str
    sensitivity: Literal["Fortrolige", "IkkeFortrolige", "SærligFølsomme", "Følsomme"]
    document_type: Literal["Indgående", "Udgående", "Internt", "Dagsordenpunkt", "Dagsorden", "Referat", "Andet", "GisKort", "NovaDagsordenspunkt"]
    description: str
    approved: bool
    document_number: Optional[str] = None
    document_date: Optional[str] = None
    file_extension: Optional[str] = None


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
class Task:
    """A dataclass representing a KMD Nova task."""
    uuid: str
    title: str
    description: Optional[str]
    case_worker_ident: Optional[str]
    case_worker_uuid: str
    status_code: Literal['F', 'N', 'S']  # Finished, Not Started, Started
    deadline: datetime
    created_date: Optional[datetime]
    started_date: Optional[datetime]
    closed_date: Optional[datetime]


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
    kle_number: str
