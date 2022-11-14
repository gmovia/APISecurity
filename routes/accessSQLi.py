from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import engine, get_db
from schema.user import UserSchema
from model import user
from config.accessSQLiCrud import verify_username_and_password

SQLi = APIRouter()

user.Base.metadata.create_all(bind=engine)

@SQLi.post("/SQLi/login/", status_code=200)
def login(user: UserSchema, db: Session = Depends(get_db)):
    response = verify_username_and_password(user, db)

    if len(response) == 0:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    return response