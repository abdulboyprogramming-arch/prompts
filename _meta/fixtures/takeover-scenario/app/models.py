"""Plain data objects. There is no ORM; queries are written by hand."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    plan: str
    created_at: datetime


@dataclass
class Report:
    id: int
    user_id: int
    payload: str
    created_at: datetime


def _fmt_date(value):
    return value.strftime("%d/%m/%Y")
