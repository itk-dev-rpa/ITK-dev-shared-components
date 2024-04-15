"""This module contains dataclasses relating to KMD Nova cases."""

from dataclasses import dataclass
from typing import Literal, Optional
from datetime import datetime

# All classes in this module are pure dataclasses made to contain data.
# pylint: disable=too-many-instance-attributes


@dataclass(slots=True, kw_only=True)
class Department:
    """A dataclass representing a department in a KMD Nova case."""
    id: int
    name: str
    user_key: str


@dataclass(slots=True, kw_only=True)
class Caseworker:
    """A dataclass representing a caseworker in a KMD Nova case."""
    uuid: str
    name: str
    ident: str


@dataclass(slots=True, kw_only=True)
class CaseParty:
    """A dataclass representing a case party in a KMD Nova case."""
    uuid: Optional[str] = None
    role: Literal["Primær", "Sekundær"]
    identification_type: Literal["CprNummer", "CvrNummer", "Frit", "PNummer", "EsrNummer", "BfeNummer"]
    identification: str
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
    document_date: Optional[datetime] = None
    file_extension: Optional[str] = None
    category_name: Optional[str] = None
    category_uuid: Optional[str] = None
    caseworker: Optional[Caseworker] = None


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
    caseworker: Caseworker
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
    caseworker: Optional[Caseworker] = None
    document_count: Optional[int] = 0
    note_count: Optional[int] = 0
    kle_number: str
    proceeding_facet: str
    sensitivity: Literal["Fortrolige", "IkkeFortrolige", "SærligFølsomme", "Følsomme"]
    responsible_department: Department
    security_unit: Department
