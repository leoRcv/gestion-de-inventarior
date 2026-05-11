import os
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Carga las variables del archivo .env
load_dotenv()

# Lee la clave secreta de forma segura
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def obtener_password_hash(password: str):
    """Convierte la contraseña en un texto ilegible"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verificar_password(plain_password: str, hashed_password: str):
    """Compara la contraseña plana con la encriptada de la BD"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def crear_token_acceso(data: dict):
    """Genera el 'Pase VIP' (JWT) para el usuario"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregamos la fecha de expiración al contenido del token
    to_encode.update({"exp": expire})
    
    # Creamos el token firmado con nuestra clave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt