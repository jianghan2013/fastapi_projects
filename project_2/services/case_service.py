from ..data_models import Case, NotesCreate, ActionCreate
from ..dependencies import get_valid_user
from ..fake_data import case_db, user_db

# store all business logics into service.py and make endpoints thin
def update_case_notes(case:Case, payload: NotesCreate):
    case_id = case.case_id
    case.notes = payload.notes
    # update DB
    case_db[case_id]["notes"] = case.notes 
    return Case(**case_db[case.case_id])

def apply_case_action(case:Case, payload: ActionCreate):
    case_id = case.case_id
    user_id = case.user_id
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