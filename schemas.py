"""importar librerias de pydantic"""
from pydantic import BaseModel, Field, EmailStr
from typing import Union, Optional
from datetime import datetime


class Dates(BaseModel):
    """Clase dates"""
    start: str
    end: str


class UserBase(BaseModel):
    """Clase UserBase"""
    email: str = Field(
        title="Email",
        description="Email del usuario",
        example="Correo@ejemplo"
    )
    name: str


class User(UserBase):
    """Clase User"""
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    """Clase TaskBase"""
    name: str
    task_url: str
    tag: Union[str, None]


class Task(TaskBase):
    """Clase Task"""
    id: str

    class Config:
        orm_mode = True


class TimeEntryBase(BaseModel):
    """Clase TimeEntryBase"""
    user_id: int
    task_id: str
    start_time: datetime
    end_time: datetime
    duration: int
    description: str


class TimeEntry(TimeEntryBase):
    """Clase TimeEntry"""
    id: int

    class Config:
        orm_mode = True


