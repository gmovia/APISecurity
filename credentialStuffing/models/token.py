from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class Token(Base):
    __tablename__ = "tokensCredentialStuffing"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("usuariosCredentialStuffing.username"))
    token = Column(Integer)
    start_date = Column(DateTime)
    user = relationship("User", back_populates="token")
    