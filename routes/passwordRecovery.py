from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db, engine
from config.accessCrud import *
from config.tokenCrud import *
from schema.passwordRecovery import PasswordRecoverySchema
from model import token

passwordRecovery = APIRouter()

token.Base.metadata.create_all(bind=engine)

@passwordRecovery.post("/get-token/", status_code=200)
def get_code(username: str, db: Session = Depends(get_db)):
    response = is_user_exist(username, db)

    if response is False:
        raise HTTPException(status_code=403, detail="User not exist.")

    return create_token(username, db)

@passwordRecovery.post("/reset-my-password/", status_code=200)
def reset_my_password(query: PasswordRecoverySchema, db: Session = Depends(get_db)):
    # Si hago fuerza bruta puedo cambiar la contraseña del usuario => Vulnerabilidad
    if is_user_exist(query.username, db) is False:
        raise HTTPException(status_code=403, detail="User not exist.")
    
    if is_the_user_token(query.username, query.token, db) is False:
        raise HTTPException(status_code=403, detail="Token incorrect.")

    return reset_password(get_user(query.username, db), query.new_password, db)

    






