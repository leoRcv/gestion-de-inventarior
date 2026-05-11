from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import usuario_repo

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=schemas.UsuarioResponse)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificamos si el correo ya existe en la base de datos
    usuario_existente = usuario_repo.obtener_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    # 2. Si no existe, lo creamos (el repo se encarga de encriptar la contraseña)
    return usuario_repo.crear_usuario(db, usuario)