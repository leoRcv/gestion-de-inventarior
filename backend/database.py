from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 🚨 CAMBIA "tu_contraseña" por la que usas en pgAdmin
# "inventario_db" es el nombre de la base de datos que creaste
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/inventario_db"

# Creamos el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos una sesión para poder hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta función la usaremos después para conectar los modelos
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()