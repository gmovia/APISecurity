from pydantic import BaseModel

class PasswordRecoverySchema(BaseModel):
    username: str
    new_password: str
    token: int
    