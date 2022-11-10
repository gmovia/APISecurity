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

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def get_user(user: UserSchema, db: Session):
    query = text("SELECT * FROM usuarios WHERE username='%s' AND password='%s'" %(user.username, user.password))
    user_list = []
    for user in engine.execute(query):
        user_list.append(user)
    return user_list
    
