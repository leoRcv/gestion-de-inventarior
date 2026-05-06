from fastapi import FastAPI
from database import engine
from models import models  # Importas tus modelos para crear las tablas
from routers import categoria_router , producto_router, venta_router    # Importas el router que creamos

# 1. ORDEN DE CONSTRUCCIÓN: 
# Al arrancar, crea las tablas en PostgreSQL basado en tus modelos
models.Base.metadata.create_all(bind=engine)

# 2. INICIALIZACIÓN:
app = FastAPI(
    title="Sistema de Gestión de Inventario - Electrónica",
    description="Backend para control de stock de mouses, cargadores y más.",
    version="1.0.0"
)

# 3. CONEXIÓN DE CAPAS:
# Registramos las rutas de categorías. 
# Esto hace que 'categoria_router.py' sea visible para el mundo.
app.include_router(categoria_router.router)
app.include_router(producto_router.router)
app.include_router(venta_router.router) 
# 4. RUTA DE BIENVENIDA (Opcional):
@app.get("/")
def inicio():
    return {"status": "Online", "negocio": "Tienda de Electrónica"}