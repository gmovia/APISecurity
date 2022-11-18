from pydantic import BaseModel

class UserRegisterSchema(BaseModel):
    username: str
    password: str
    phone: str
    
class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserNewPasswordSchema(BaseModel):
    username: str
    new_password: str
    pin: str