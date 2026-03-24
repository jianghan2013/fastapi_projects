#
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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


def get_valid_case(case_id: int) -> Case:
    if case_id in case_db:
        return Case(**case_db[case_id])
    else:
        raise HTTPException(status_code=404, detail="Case not found") 


def get_valid_user(user_id: int) -> User:
    if user_id in user_db:
        return User(**user_db[user_id])
    else:
        raise HTTPException(status_code=404, detail="User not found") 


# return a list of cases
@app.get("/cases", response_model=list[Case])
async def get_cases():
    cases =[]
    for i in case_db:
        cases.append(Case(**case_db[i]))
    return cases


# use case_id instead of case type, since case_id is a path parameter associated with a GET method
# case_id is now shown in the dependency function
@app.get("/cases/{case_id}", response_model=Case)
async def get_case(case: Annotated[Case, Depends(get_valid_case)]):
    return case

# make the notes as a request parameter instead of a query parameter    
@app.post("/cases/{case_id}/notes", response_model=Case)
async def write_notes(payload: NotesCreate, case: Annotated[Case, Depends(get_valid_case)]):
    case_id = case.case_id
    case.notes = payload.notes
    # update DB
    case_db[case_id]["notes"] = case.notes 
    return case

# this include take action as well as reinstated
# use patch since it only update partially
@app.patch("/cases/{case_id}/action", response_model=Case)
async def take_action(payload: ActionCreate, case: Annotated[Case, Depends(get_valid_case)]):
    case_id = case.case_id
    user_id = case.user_id
    user = get_valid_user(user_id)
    # For simplicity, it takes action regardless of current user disabled state. 
    # Also for simplicity, it doesn't require add notes
    if payload.action: 
        user.disabled = True
        case.action = True
        # update DBs
        case_db[case_id]["action"] = case.action
        user_db[user_id]["disabled"] = user.disabled
    # this covers reinstatement
    else:
        user.disabled = False
        case.action = False
        # update DB
        case_db[case_id]["action"] = case.action
        user_db[user_id]["disabled"] = user.disabled
    return Case(**case_db[case.case_id]) # to simulate sql refresh



