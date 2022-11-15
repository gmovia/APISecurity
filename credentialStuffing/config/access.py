from fastapi import HTTPException
from schemas.user import RegisterUserSchema, LoginUserSchema
from models.user import User
from models.token import Token
from sqlalchemy.orm import Session
import random

def create_user(user: RegisterUserSchema, db: Session):
    user = User(username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id, db)
    return token

def create_token(user_id: int, db: Session):
    token = Token(user_id=user_id, token=random.randint(100000, 999999))
    db.add(token)
    db.commit()
    db.refresh(token)
    return token.token

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def verify_login(user: LoginUserSchema, db: Session):
    response = db.query(User, Token).filter(User.id == Token.user_id).filter(User.username == user.username).filter(User.password == user.password).filter(Token.token == user.token).first()
    return response

def the_password_is_valid(password: str):
    return(len(password) >= 8 and password.isalnum() and password.islower()==False)
