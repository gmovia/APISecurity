from fastapi import HTTPException
from schemas.user import RegisterUserSchema, LoginUserSchema
from models.user import User
from models.token import Token
from sqlalchemy.orm import Session
import pyautogui, webbrowser
from time import sleep
import random
import datetime

def create_user(user: RegisterUserSchema, db: Session):
    user = User(username=user.username, password=user.password, phone=user.phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def create_token(username: str, db: Session):
    user_db = get_user(username, db)
    token = Token(username=username, token=random.randint(100000, 999999), start_date=datetime.datetime.now())
    db.add(token)
    db.commit()
    db.refresh(token)
    send_token(token.token, user_db.phone)

def is_token_correct(username: str, token: int, db: Session):
    refresh_token(username, db)
    return db.query(Token).filter(Token.username == username).filter(Token.token == token).first() is not None

def refresh_token(username: str, db: Session):
    token_db = db.query(Token).filter(Token.username == username).first()
    if((datetime.datetime.now() - token_db.start_date).seconds > 120):
        db.delete(token_db)
        db.commit()

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def verify_login(user: LoginUserSchema, db: Session):
    response = db.query(User, Token).filter(User.username == Token.username).filter(User.username == user.username).filter(User.password == user.password).filter(Token.token == user.token).first()
    return response

def the_password_is_valid(password: str):
    return(len(password) >= 8 and password.isalnum() and password.islower()==False)

def send_token(token: int, phone: str): 
    webbrowser.open('https://web.whatsapp.com/send?phone='+phone)
    sleep(5)
    pyautogui.typewrite(str(token))
    pyautogui.press('enter')