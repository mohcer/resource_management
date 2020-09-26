"""
Problem Domain

This Service handles all crud operation to save retrive dumped auth tokens
"""
from ...main import db
from ..model.token_garbage import TokenGarbage


# dump this token
def dump_token(auth_token):
    invalid_token = TokenGarbage(auth_token)
    try:
        # save this token
        db.session.add(invalid_token)
        db.session.commit()

        res_obj = {"status": "success", "message": "successfully logged out!"}

        return res_obj, 200
    except Exception as e:
        res_obj = {"status": "fail", "message": str(e)}

        return res_obj, 200
