from fastapi import Depends, APIRouter
from pydantic import BaseModel
from typing import Annotated
from ..dependencies import *


router = APIRouter()


# return a list of cases
@router.get("/cases", response_model=list[Case], tags=["cases"])
async def get_cases():
    cases =[]
    for i in case_db:
        cases.append(Case(**case_db[i]))
    return cases


# use case_id instead of case type, since case_id is a path parameter associated with a GET method
# case_id is now shown in the dependency function
@router.get("/cases/{case_id}", response_model=Case, tags=["cases"])
async def get_case(case: Annotated[Case, Depends(get_valid_case)]):
    return case


# make the notes as a request parameter instead of a query parameter    
@router.post("/cases/{case_id}/notes", response_model=Case, tags=["cases"])
async def write_notes(payload: NotesCreate, case: Annotated[Case, Depends(get_valid_case)]):
    case_id = case.case_id
    case.notes = payload.notes
    # update DB
    case_db[case_id]["notes"] = case.notes 
    return case

# this include take action as well as reinstated
# use patch since it only update partially
@router.patch("/cases/{case_id}/action", response_model=Case, tags=["cases"])
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