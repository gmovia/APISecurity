from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Token(Base):
    __tablename__ = "tokensCredentialStuffing"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuariosCredentialStuffing.id"))
    token = Column(Integer)
    user = relationship("User", back_populates="token")
    