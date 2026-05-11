import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carga las variables del archivo .env
load_dotenv()

# Lee la URL de la base de datos de forma segura
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ¡ESTA ES LA FUNCIÓN QUE FALTABA! ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()