from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from schema.user import UserSchema
from config.accessCrud import *

access = APIRouter()

@access.post("/register/", status_code=200)
def register(user: UserSchema, db: Session = Depends(get_db)):
    response = is_user_exist(user.username, db)

    if response is True:
        raise HTTPException(status_code=403, detail="Already registered user.")

    return create_user(user, db).id

@access.post("/login/", status_code=200)
def login(user: UserSchema, db: Session = Depends(get_db)):
    response = verify_username_and_password(user, db)

    if response is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    return response

