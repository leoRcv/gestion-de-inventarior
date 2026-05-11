from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from repositories import usuario_repo
from security import verificar_password, crear_token_acceso
from schemas import schemas

router = APIRouter(tags=["Autenticación"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscamos al usuario en la BD. 
    # (Nota: FastAPI usa 'username' por defecto, nosotros le pasaremos el email ahí)
    usuario = usuario_repo.obtener_usuario_por_email(db, email=form_data.username)
    
    # 2. Verificamos que el usuario exista y que la contraseña coincida
    if not usuario or not verificar_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Si todo está OK, fabricamos el Pase VIP (Token)
    # Guardamos el email y el rol dentro del token para saber quién es
    datos_token = {"sub": usuario.email, "rol": usuario.rol}
    token_generado = crear_token_acceso(data=datos_token)
    
    # 4. Entregamos el token
    return {"access_token": token_generado, "token_type": "bearer"}