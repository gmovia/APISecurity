from pydantic import BaseModel

class RegisterUserSchema(BaseModel):
    username: str
    password: str
    phone: str
    
class LoginUserSchema(BaseModel):
    username: str
    password: str
    token: int