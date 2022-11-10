from sqlalchemy import Column, Integer, String
from config.db import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)