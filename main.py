import json
from time import gmtime
from datetime import time, datetime
from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import schemas
import models
import bd_transactions
from database import SessionLocal, engine
from typing import List, Union
from pydantic import Field
import requests


# ID de Sioma en clickup
ID_SIOMA = 31035720
# API token de clickup
API_TOKEN = "pk_43152028_XMRZMC6A3ZPTV2LV1ZZIC4ZA5USTFVA8"

# Crear tablas
#

# Funciones

def get_users():
    """Importar usuarios de archivo .json"""
    with open('members.json') as f:
        users = json.load(f)['members']
    return users


def clean_users(users):
    """Obtener solo los campos necesarios de los usuarios"""
    clean_users = []
    for user in users:
        clean_user = {
            'id': user['id'],
            'email': user['email'],
            'name': user['username'],
        }
        clean_users.append(clean_user)
    return clean_users


# Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_millis(date):
    """
    obtener milisegundos a partir de una fecha
    """
    # agregar tiempo a la fecha si no tiene
    if len(date) == 10:
        date = date + ' 00:00:00'
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return int(date.timestamp() * 1000)


def get_date(milliseconds):
    """
    Obtener fecha a partir de milisegundos
    """
    return datetime.fromtimestamp(int(milliseconds) / 1000.0)


def get_time_entries(start_date, end_date, user_id):
    """funcion para obtener las entradas de tiempo de la api de clickup usando la libreria requests"""
    headers = {'Authorization': API_TOKEN}
    url = f'https://api.clickup.com/api/v2/team/{ID_SIOMA}/time_entries'
    params = {
        'start_date': get_millis(start_date),
        'end_date': get_millis(end_date),
        'assignee': user_id,
        'include_task_tags': 'true'
              }
    response = requests.get(url, headers=headers, params=params)
    return response.json()




app = FastAPI()

# agregar cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rutas
@app.get("/")
async def root():
    return {"message": "Estoy andando bien cabron"}


@app.get("/update_users")
async def update_users(db: Session = Depends(get_db)):
    """Actualizar usuarios en la base de datos"""
    users = get_users()
    users_clean = clean_users(users)
    inserted_users = 0
    for user in users_clean:
        if bd_transactions.insert_user(db, schemas.User(**user)):
            inserted_users += 1
    return {"usuarios insertados": inserted_users}


@app.post("/update_time_entries")
async def update_time_entries(
        user_id: Union[int, None] = Query(None, description="ID del usuario"),
        fechas: schemas.Dates = Body(..., description="Rango de fechas"),
        db: Session = Depends(get_db)
):
    """Obtener entradas de tiempo de la api de clickup y actualizarlas en la base de datos"""
    if user_id:
        users = [user_id]
    else:
        users = [user['id'] for user in get_users()]
    inserted_time_entries = 0
    inserted_tasks = 0
    for user in users:
        time_entries = get_time_entries(fechas.start, fechas.end, user)
        if time_entries['data']:
            for time_entry in time_entries['data']:
                # obtener los campos necesarios del schema TimeEntry
                time_entry_bd = {
                    'id': time_entry['id'],
                    'user_id': time_entry['user']['id'],
                    'task_id': time_entry['task']['id'],
                    'start_time': get_date(time_entry['start']),
                    'end_time': get_date(time_entry['end']),
                    'duration': time_entry['duration'],
                    'description': time_entry['description']
                }
                # obtener los datos de la tarea desde time_entry
                task = {
                    'id': time_entry['task']['id'],
                    'name': time_entry['task']['name'],
                    'tags': time_entry['task_tags'][0]['name'] if time_entry['task_tags'] else None,
                    'task_url': time_entry['task_url']
                }
                # Transacciones
                if bd_transactions.insert_task(db, schemas.Task(**task)):
                    inserted_tasks += 1
                if bd_transactions.insert_time_entry(db, schemas.TimeEntry(**time_entry_bd)):
                    inserted_time_entries += 1

    return {"entradas de tiempo insertadas": inserted_time_entries, "tareas insertadas": inserted_tasks}


@app.post("/time_by_user")
async def time_by_user(
        user_id: Union[int, None] = Query(None, description="ID del usuario"),
        fechas: schemas.Dates = Body(..., description="Rango de fechas"),
        db: Session = Depends(get_db)
):
    """Obtener duracion total de las entradas de tiempo de un usuario desde la bd"""
    if user_id:
        users = [user_id]
    else:
        users = [user['id'] for user in get_users()]
    duration_by_user = []
    for user in users:
        bd_result = bd_transactions.get_duration_by_user_id(fechas.start, fechas.end, user, db)
        bd_result[0][2] = time.strftime('%H:%M:%S', gmtime(bd_result[0][2] / 1000))
        duration_by_user.append(bd_result)
    print(duration_by_user)
    return duration_by_user

