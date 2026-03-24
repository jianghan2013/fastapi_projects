from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    disabled: bool | None = None

class NotesCreate(BaseModel):
    notes: str | None = None

class ActionCreate(BaseModel):
    action: bool

class Case(BaseModel):
    case_id: int 
    user_id: int | None = None 
    action: bool | None = None
    explain: str | None = None
    notes: str | None = None