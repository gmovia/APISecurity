from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db, engine
from schemas.user import *
from config.access import *
from models import user

access = APIRouter()

user.Base.metadata.create_all(bind=engine)

@access.post("/register/", status_code=200)
def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    response = is_user_exist(user.username, db)

    if response is True:
        raise HTTPException(status_code=403, detail="Already registered user.")

    return create_user(user, db).id

@access.post("/login/", status_code=200)
def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    response = verify_username_and_password(user, db)

    if response is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    return response

@access.post("/get-pin-to-reset-password/")
def get_pin(username: str, db: Session = Depends(get_db)):
    response = is_user_exist(username, db)

    if response is False:
        raise HTTPException(status_code=403, detail="User not exist.")

    return generate_pin(username, db)
    
@access.post("/generate-new-password/")
def generate_new_password(user: UserNewPasswordSchema, db: Session = Depends(get_db)):
    response = is_user_exist(user.username, db)

    if response is False:
        raise HTTPException(status_code=403, detail="User not exist.")
    
    if is_pin_correct(user.username, user.pin, db) is False:
        raise HTTPException(status_code=403, detail="PIN invalid.")
    
    change_password(user.username, user.new_password, db)

    return "OK"

from sqlalchemy import text
@access.get('/delete/')
def delete():
    with engine.connect() as c:
        c.execute(text("DROP TABLE usuariosPW"))
        c.execute(text("DROP TABLE pinPW"))