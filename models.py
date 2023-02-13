"""importar tipos de sqlalchemy"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, DECIMAL, BigInteger
from sqlalchemy.orm import relationship
"""importar la base de datos"""
from database import Base


class TimeEntries(Base):
    """Clase TimeEntries"""
    __tablename__ = "TimeEntries"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("Users.id"))
    task_id = Column(String(48), ForeignKey("Tasks.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)
    description = Column(String(212), index=True)

    _Users = relationship("Users", back_populates="time_entries")
    _Tasks = relationship("Tasks", back_populates="time_entries")

    class Config:
        orm_mode = True



class Users(Base):
    """Clase Users"""
    __tablename__ = "Users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(48), unique=True, index=True)
    name = Column(String(48), index=True)

    time_entries = relationship("TimeEntries", back_populates="_Users")


    class Config:
        orm_mode = True


class Tasks(Base):
    """Clase Tasks"""
    __tablename__ = "Tasks"

    id = Column(String(48), primary_key=True, index=True)
    name = Column(String(512), index=True)
    task_url = Column(String(212), index=True)
    tag = Column(String(48), index=True)

    time_entries = relationship("TimeEntries", back_populates="_Tasks")

    class Config:
        orm_mode = True

