from schema.user import UserSchema
from model.user import User
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.db import engine

def create_user(user: UserSchema, db: Session):
    user = User(username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

