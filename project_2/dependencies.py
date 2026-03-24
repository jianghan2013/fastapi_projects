from fastapi import HTTPException
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


user_db = {
    11: {
        "user_id": 11,
        "disabled": False
    },
    22: {
        "user_id": 22,
        "disabled": False
    },
    33: {
        "user_id": 33,
        "disabled": False
    },
}

case_db = {
    1: {
     "case_id": 1,
     "user_id": 11,
     "action": None,
     "explain": "high score",
     "notes": None
    },
    2: {
     "case_id": 2,
     "user_id": 22,
     "action": None,
     "explain": "linked entity",
     "notes": None,
    },
    3: {
     "case_id": 3,
     "user_id": 33,
     "action": None,
     "explain": "abnormal velocity",
     "notes": None
    }
}


def get_valid_case(case_id: int):
    if case_id in case_db:
        return Case(**case_db[case_id])
    else:
        raise HTTPException(status_code=404, detail="Case not found") 


def get_valid_user(user_id: int):
    if user_id in user_db:
        return User(**user_db[user_id])
    else:
        raise HTTPException(status_code=404, detail="User not found")