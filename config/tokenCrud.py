from schema.user import UserSchema
from model.token import Token
from sqlalchemy.orm import Session
import random

def create_token(username: str, db: Session):
    token = Token(username=username, token=random.randint(100000, 999999)) 
    db.add(token)
    db.commit()
    db.refresh(token)
    return token.token

def get_token(username: str, db: Session):
    return db.query(Token.token).filter(Token.username == username).first()

def is_the_user_token(username: str, token: int, db: Session):
    return db.query(Token).filter(Token.username == username).filter(Token.token == token).first() is not None