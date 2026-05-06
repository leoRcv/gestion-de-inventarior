from sqlalchemy.orm import Session
from models import models # Importamos tus tablas
from schemas import schemas # Importamos tus moldes

# Función para guardar una categoría nueva
def crear_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Función para traer todas las categorías (útil para desplegables)
def obtener_categorias(db: Session):
    return db.query(models.Categoria).all()