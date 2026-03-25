from fastapi import HTTPException
from .fake_data import case_db, user_db
from .data_models import Case, User
from typing import Annotated
from fastapi import Depends


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

# user -> get_valid_user -> case -> Case -> get_valid_case
def get_user_from_case(
    case: Annotated[Case, Depends(get_valid_case)]
    ) -> User:
    return get_valid_user(case.user_id)