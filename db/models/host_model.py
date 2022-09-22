from sqlalchemy import Integer, String, Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..db_setup import Base


class HostModel(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(Text)
    route = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='hosts')
