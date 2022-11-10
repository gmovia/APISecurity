from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserSchema
from config.crud import *
from model import user
from config.db import engine, get_db

app = FastAPI()

user.Base.metadata.create_all(bind=engine)

@app.post("/login/", status_code=200)
def login(user: UserSchema, db: Session = Depends(get_db)):
    user_db = get_user(user.username, db)

    if user_db is None or user_db.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    return user_db


@app.post("/register/", status_code=200)
def register(user: UserSchema, db: Session = Depends(get_db)):
    user_db = get_user(user.username, db)

    if user_db is not None:
        raise HTTPException(status_code=403, detail="Already registered user.")

    return create_user(user, db).id