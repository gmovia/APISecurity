from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db, engine
from schemas.user import *
from config.access import *
from models import user
from models import token

access = APIRouter()

user.Base.metadata.create_all(bind=engine)
token.Base.metadata.create_all(bind=engine)

@access.post("/register/", status_code=200)
def register(user: RegisterUserSchema, db: Session = Depends(get_db)):
    response = is_user_exist(user.username, db)

    if response is True:
        raise HTTPException(status_code=403, detail="Already registered user.")

    if the_password_is_valid(user.password) is False:
        raise HTTPException(status_code=403, detail="Permission denied.")

    return create_user(user, db)

@access.post("/login/", status_code=200)
def login(user: LoginUserSchema, db: Session = Depends(get_db)):
    response = verify_login(user, db)
    
    if response is None:
        raise HTTPException(status_code=401, detail="Incorrect email, password or token.")
    
    return response.User

from sqlalchemy import text
@access.delete('/deleteDataBase/')
def delete():
    with engine.connect() as c:
        c.execute(text("DROP TABLE usuariosCredentialStuffing"))
        c.execute(text("DROP TABLE tokensCredentialStuffing"))