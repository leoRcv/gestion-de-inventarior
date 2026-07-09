from database import SessionLocal 
from models.models import Usuario  
from security import obtener_password_hash 

def crear_usuario_prueba():
    db = SessionLocal()
    try:
        # Ponemos tus datos reales basados en tu modelo de la foto
        nombre_prueba = "Jorge Admin"
        email_prueba = "admin@inventario.com" # <--- Este será tu "usuario/email" en el Login
        password_claro = "admin123"           # <--- Tu contraseña en React
        
        # Ciframos la contraseña usando tu función del backend
        password_cifrada = obtener_password_hash(password_claro)
        
        # Creamos la instancia con las columnas EXACTAS de tu clase Usuario
        nuevo_usuario = Usuario(
            nombre=nombre_prueba,
            email=email_prueba,
            hashed_password=password_cifrada,
            rol="admin", # Le mandamos 'admin' directamente para tener todos los permisos
            is_active=True
        )
        
        db.add(nuevo_usuario)
        db.commit()
        print("¡Usuario de prueba creado con éxito!")
        print(f"Email/Usuario: {email_prueba}")
        print(f"Contraseña: {password_claro}")
        
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_prueba()