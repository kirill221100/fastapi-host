from sqlalchemy import Integer, String, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..db_setup import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    token = Column(String)
    hosts = relationship("HostModel", back_populates='user')
