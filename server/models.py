# imports
from pydantic import BaseModel
from typing import Optional

# class for clean records
class CleanRecord(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    start_date: str
    active: bool
    course: str

# class for invalid records
class InvalidRecord(BaseModel):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    start_date: Optional[str]
    active: Optional[bool]
    course: Optional[str]