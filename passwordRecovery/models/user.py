from sqlalchemy import Column, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "usuariosPW"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    phone = Column(String)
    pin = relationship("PIN", back_populates="user")