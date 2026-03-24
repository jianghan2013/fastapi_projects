agents fetch cases, read evidence, add notes, and action or no action 

end points like 
GET /cases
GET /cases/{case_id}
POST /cases/{case_id}/action
POST /cases/{case_id}/notes
POST /cases/{case_id}/explain

# let's restrict the user to be only the flagged users

resources:
- user: user_id, user_name, score, disabled = True
- case: case_id: int, user_id: int, queue:str, is_review: bool, action = bool

operation
- 