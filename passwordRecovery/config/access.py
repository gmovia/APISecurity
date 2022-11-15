from schemas.user import *
from models.user import User
from models.PIN import PIN
from sqlalchemy.orm import Session
import random
import pyautogui, webbrowser
from time import sleep
import datetime

def create_user(user: UserRegisterSchema, db: Session):
    user = User(username=user.username, password=user.password, phone=user.phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def is_user_exist(username:str, db: Session):
    return db.query(User).filter(User.username == username).first() is not None

def get_phone_by_username(username: str, db: Session):
    return db.query(User.phone).filter(User.username == username).first()

def verify_username_and_password(user: UserLoginSchema, db: Session):
    return db.query(User).filter(User.username == user.username).filter(User.password == user.password).first()

def generate_pin(username: str, db: Session):
    pin = random.randint(100000000000, 999999999999)
    pin_db = PIN(pin=pin, username=username, start_date=datetime.datetime.now())
    db.add(pin_db)
    db.commit()
    db.refresh(pin_db)
    send_pin(pin, get_phone_by_username(username, db).phone)
    return "OK"

def is_pin_correct(username: str, pin: int, db: Session):
    refresh_pin(username, db)
    return db.query(PIN).filter(PIN.username == username).filter(PIN.pin == pin).first() is not None

def refresh_pin(username: str, db: Session):
    pin_db = db.query(PIN).filter(PIN.username == username).first()
    if((datetime.datetime.now() - pin_db.start_date).seconds > 120):
        db.delete(pin_db)
        db.commit()

def change_password(username: str, new_password: str, db: Session):
    user_db = get_user(username, db)
    user_db.password = new_password
    db.add(user_db)
    db.commit()

def send_pin(pin: int, phone: str): #+54911+telefono
    webbrowser.open('https://web.whatsapp.com/send?phone='+phone)
    sleep(5)
    pyautogui.typewrite(str(pin))
    pyautogui.press('enter')