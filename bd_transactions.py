"""importar librerias de sqlalchemy"""
from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy import func
from database import SessionLocal, engine


def get_user(db: Session, user_id: int):
    """Obtener usuario por id"""
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Obtener usuario por email"""
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtener usuarios"""
    return db.query(models.Users).offset(skip).limit(limit).all()


def insert_user(db: Session, user: schemas.User):
    """Insertar usuario"""
    db_user = models.Users(id=user.id, email=user.email, name=user.name)
    """Validar si el usuario ya existe usando el id, levantar excepcion si es asi y no insertar"""
    if not get_user(db, user.id):
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def get_task(db: Session, task_id: int):
    """Obtener tarea por id"""
    return db.query(models.Tasks).filter(models.Tasks.id == task_id).first()


def insert_task(db: Session, task: schemas.Task):
    """Insertar tarea"""
    db_task = models.Tasks(id=task.id, name=task.name, tag=task.tag, task_url=task.task_url)
    # validar si la tarea ya existe usando el id, levantar excepcion si es asi y no insertar
    if not get_task(db, task.id):
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    return db_task


def get_time_entry(db, id):
    """Obtener entrada de tiempo por id"""
    return db.query(models.TimeEntries).filter(models.TimeEntries.id == id).first()


def insert_time_entry(db: Session, time_entry: schemas.TimeEntry):
    """Insertar entrada de tiempo"""
    db_time_entry = models.TimeEntries(
        id=time_entry.id,
        user_id=time_entry.user_id,
        task_id=time_entry.task_id,
        start_time=time_entry.start_time,
        end_time=time_entry.end_time,
        duration=time_entry.duration,
        description=time_entry.description,
    )
    # validar si la entrada de tiempo ya existe usando el id, levantar excepcion si es asi y no insertar
    if not get_time_entry(db, time_entry.id):
        db.add(db_time_entry)
        db.commit()
        db.refresh(db_time_entry)
        return db_time_entry


def get_time_entries_by_user_id(start_date, end_date, db: Session, user_id: int):
    """Obtener el total de tiempo trabajado en cada tarea por usuario en un rango de fechas"""
    return (
        db.query(
            models.TimeEntries.task_id,
            models.TimeEntries.user_id,
            models.Tasks.name,
            models.Tasks.tag,
            models.Tasks.task_url,
            models.Users.name,
            models.Users.email,
            func.sum(models.TimeEntries.duration),
        )
        .filter(
            models.TimeEntries.user_id == user_id,
            models.TimeEntries.start_time >= start_date,
            models.TimeEntries.end_time <= end_date,
        )
        .join(models.Users, models.TimeEntries.user_id == models.Users.id)
        .join(models.Tasks, models.TimeEntries.task_id == models.Tasks.id)
        .group_by(models.TimeEntries.task_id)
        .all()
    )


def get_duration_by_user_id(start_date, end_date, user_id: int, db: Session):
    """Obtener el total de tiempo trabajado por usuario en un rango de fechas"""
    return (
        db.query(
            models.TimeEntries.user_id,
            models.Users.name,
            func.sum(models.TimeEntries.duration),
        )
        .filter(
            models.TimeEntries.user_id == user_id,
            models.TimeEntries.start_time >= start_date,
            models.TimeEntries.end_time <= end_date,
        )
        .join(models.Users, models.TimeEntries.user_id == models.Users.id)
        .group_by(models.TimeEntries.user_id, models.Users.name)
        .all()
    )


