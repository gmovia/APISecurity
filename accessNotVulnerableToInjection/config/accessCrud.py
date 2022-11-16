from schemas.user import UserSchema
from models.user import User
from sqlalchemy.orm import Session

def create_user(user: UserSchema, db: Session):
    user = User(username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def verify_username_and_password(user: UserSchema, db: Session):
    return db.query(User).filter(User.username == user.username).filter(User.password == user.password).first()