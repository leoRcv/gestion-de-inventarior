from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from repositories import usuario_repo
from security import SECRET_KEY, ALGORITHM
from models import models

# Le decimos a FastAPI dónde se consiguen los tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# GUARDIA 1: Verifica que el token sea real y busca quién eres
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Desencriptamos el token para leer el email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise excepcion_credenciales
    except JWTError:
        raise excepcion_credenciales
        
    # Buscamos al usuario en la base de datos
    usuario = usuario_repo.obtener_usuario_por_email(db, email=email)
    if usuario is None:
        raise excepcion_credenciales
    return usuario

# GUARDIA 2: Verifica que tu rol sea "admin"
def verificar_admin(usuario_actual: models.Usuario = Depends(obtener_usuario_actual)):
    if usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes (Solo Admin)"
        )
    return usuario_actual