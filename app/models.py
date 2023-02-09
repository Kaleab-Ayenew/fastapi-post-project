from .database import Base
from sqlalchemy import Column
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    draft = Column(Boolean, nullable=False, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    # id = Column(Integer, primary_key=True, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
