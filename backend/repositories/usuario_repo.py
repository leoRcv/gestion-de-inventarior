from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from security import obtener_password_hash

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # 1. Encriptamos la contraseña que viene del schema
    hashed_pwd = obtener_password_hash(usuario.password)
    
    # 2. Creamos el modelo de base de datos, reemplazando el password por el hash
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hashed_pwd,
        rol=usuario.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuario_por_email(db: Session, email: str):
    # Esta función nos servirá para el Login más adelante
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()