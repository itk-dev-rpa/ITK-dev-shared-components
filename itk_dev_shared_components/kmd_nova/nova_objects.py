"""This module contains dataclasses relating to KMD Nova cases."""

from dataclasses import dataclass
from typing import Literal, Optional
from datetime import datetime

# All classes in this module are pure dataclasses made to contain data.
# pylint: disable=too-many-instance-attributes


@dataclass(slots=True, kw_only=True)
class CaseParty:
    """A dataclass representing a case party in a KMD Nova case."""
    uuid: Optional[str] = None
    role: str
    identification_type: Optional[str] = None
    identification: Optional[str] = None
    name: Optional[str] = None


@dataclass(slots=True, kw_only=True)
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
    category_name: Optional[str] = None
    category_uuid: Optional[str] = None


@dataclass(slots=True, kw_only=True)
class JournalNote:
    """A dataclass representing a KMD Nova journal note."""
    uuid: str
    title: str
    journal_date: str
    note_format: str
    note: bytes
    approved: bool


@dataclass(slots=True, kw_only=True)
class Task:
    """A dataclass representing a KMD Nova task."""
    uuid: str
    title: str
    description: Optional[str] = None
    case_worker_ident: Optional[str] = None
    case_worker_uuid: str
    status_code: Literal['N', 'S', 'F']  # Not Started, Started, Finished
    deadline: datetime
    created_date: Optional[datetime] = None
    started_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None


@dataclass(slots=True, kw_only=True)
class NovaCase:
    """A dataclass representing a KMD Nova case."""
    uuid: str
    title: str
    case_number: Optional[str] = None
    case_date: datetime
    active_code: Optional[str] = None
    progress_state: Literal["Opstaaet", "Oplyst", "Afgjort", "Bestilt", "Udfoert", "Afsluttet"]
    case_parties: list[CaseParty]
    document_count: Optional[int] = 0
    note_count: Optional[int] = 0
    kle_number: str
    proceeding_facet: str
    sensitivity: Literal["Fortrolige", "IkkeFortrolige", "SærligFølsomme", "Følsomme"]
