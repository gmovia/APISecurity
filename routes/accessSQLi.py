from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import engine, get_db
from schema.user import UserSchema
from model import user
from config.accessSQLiCrud import get_user

SQLi = APIRouter()

user.Base.metadata.create_all(bind=engine)

@SQLi.post("/SQLi/login/", status_code=200)
def login(user: UserSchema, db: Session = Depends(get_db)):
    user_db = get_user(user, db)

    if len(user_db) == 0:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    return user_db