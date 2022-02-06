from sqlalchemy import Column
from sqlalchemy import BigInteger, Text, Boolean, DateTime
from sqlalchemy import false
from sqlalchemy.sql.functions import now

from .base import Base


class User(Base):
    __tablename__ = 'users'
    
    tg_id = Column(BigInteger, primary_key=True)

    username = Column(Text, unique=True)
    banned = Column(Boolean, nullable=False, default=false())
    created_at = Column(DateTime, nullable=False, server_default=now())
    
    def __repr__(self):
        return f"User({self.tg_id}, {self.username}, {self.banned})"
