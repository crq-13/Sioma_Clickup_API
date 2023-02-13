"""import sqlalchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Parametro de desarrollo
DEV = False


# """URL de la base de datos mysql"""
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://sioma_cristian:b08c8c585b6d67164c163767076445d6@" \
#                           "sioma-app.mysql.database.azure.com:3306/sioma_app"
# if DEV:
#     SQLALCHEMY_DATABASE_URL = "mysql+pymysql://sioma_cristian:b08c8c585b6d67164c163767076445d6@" \
#                               "sioma-dev.mysql.database.azure.com:3306/sioma_app"

"""URL de la base de datos postgresql"""
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:hEzfPM2P7PYwYt@clickupdb.crqinvest.com/clickup"
if DEV:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:hEzfPM2P7PYwYt@clickupdb.crqinvest.com/clickup_dev"


"""Crear el motor de la base de datos"""
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""Crear una sesión local"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""Crear la base"""
Base = declarative_base()

