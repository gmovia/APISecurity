from fastapi import HTTPException
from schemas.user import RegisterUserSchema, LoginUserSchema
from models.user import User
from models.token import Token
from sqlalchemy.orm import Session
import random
import smtplib
from decouple import config

def create_user(user: RegisterUserSchema, db: Session):
    user = User(username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id, db)
    return token

def create_token(user_id: int, db: Session):
    token = Token(user_id=user_id, token=random.randint(100000, 999999), attemps=5)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token.token

def numberOfAttempsIsZero(user: LoginUserSchema, db: Session):
    token = db.query(Token).join(User).filter(User.username == user.username).filter(Token.user_id == User.id).first()
    return token.attemps == 0

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def verify_login(user: LoginUserSchema, db: Session):
    if numberOfAttempsIsZero(user, db) is True:
        #send_email() // * REVISAR * //
        raise HTTPException(status_code=401, detail="Attempts is zer0.")

    response = db.query(User, Token).filter(User.id == Token.user_id).filter(User.username == user.username).filter(User.password == user.password).filter(Token.token == user.token).first()
    
    if response is None:
        decrease_attemps(user, db)
    return response

def decrease_attemps(user: LoginUserSchema, db: Session):
    response = db.query(User, Token).filter(User.username == user.username).filter(User.id == Token.user_id).first()
    if(response.Token.attemps > 0):
        response.Token.attemps -= 1
        db.add(response.Token)
        db.commit()

def send_email(): # No funca
    message = "Intentaron ingresar a su cuenta. Por favor, restablezca su contraseña"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('criptografia.tp.fiuba@gmail.com', config('MAIL_PASSWORD'))
    server.sendmail('criptografia.tp.fiuba@gmail.com', 'criptografia.tp.fiuba@gmail.com', message)
    server.quit()