from schema.user import UserSchema
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.db import engine

def get_user(user: UserSchema, db: Session):
    query = text("SELECT * FROM usuarios WHERE username='%s' AND password='%s'" %(user.username, user.password))
    user_list = []
    for user in engine.execute(query):
        user_list.append(user)
    return user_list