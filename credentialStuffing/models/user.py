from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    __tablename__ = "usuariosCredentialStuffing"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    token = relationship("Token", back_populates="user")
