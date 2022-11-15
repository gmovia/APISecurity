from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from config.db import Base
from sqlalchemy.orm import relationship

class PIN(Base):
    __tablename__ = "pinPW"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("usuariosPW.username"))
    pin = Column(Integer)
    start_date = Column(DateTime)
    user = relationship("User", back_populates="pin")
    