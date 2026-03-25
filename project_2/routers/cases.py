from fastapi import Depends, APIRouter
from typing import Annotated
from ..dependencies import get_valid_case, get_user_from_case
from ..data_models import Case, User, NotesCreate, ActionCreate
from ..services.case_service import  update_case_notes, apply_case_action


# this will add the prefix for each endpoint
router = APIRouter(prefix="/cases", tags=["cases"])


# return a list of cases
@router.get("", response_model=list[Case])
async def get_cases():
    return [Case(**case_db[i]) for i in case_db]


# use case_id instead of case type, since case_id is a path parameter associated with a GET method
# case_id is now shown in the dependency function
@router.get("/{case_id}", response_model=Case)
async def get_case(case: Annotated[Case, Depends(get_valid_case)]):
    return case


# make the notes as a request parameter instead of a query parameter    
@router.post("/{case_id}/notes", response_model=Case)
async def write_notes(
    payload: NotesCreate,
    case: Annotated[Case, Depends(get_valid_case)]
):
    return update_case_notes(case, payload)


# this include take action as well as reinstated
# use patch since it only update partially
@router.patch("/{case_id}/action", response_model=Case)
async def take_action(
    payload: ActionCreate,
    case: Annotated[Case, Depends(get_valid_case)],
    user: Annotated[User, Depends(get_user_from_case)]
):
    return apply_case_action(case, payload)