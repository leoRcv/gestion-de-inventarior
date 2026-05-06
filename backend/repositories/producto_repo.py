from sqlalchemy.orm import Session
from models import models
from schemas import schemas

def crear_producto(db: Session, producto: schemas.ProductoCreate):
    # 1. Creamos el producto
    nuevo_p = models.Producto(**producto.model_dump())
    db.add(nuevo_p)
    db.commit()
    db.refresh(nuevo_p)

    # 2. Lógica Automática: Registramos el movimiento inicial
    nuevo_movimiento = models.Movimiento(
        producto_id=nuevo_p.id,
        tipo="ENTRADA",
        cantidad=nuevo_p.stock_actual,
        motivo="Stock inicial de creación"
    )
    db.add(nuevo_movimiento)
    db.commit()
    
    return nuevo_p

# Nueva función para ver el historial
def obtener_historial_movimientos(db: Session, producto_id: int):
    return db.query(models.Movimiento).filter(models.Movimiento.producto_id == producto_id).all()

def obtener_por_codigo(db: Session, codigo: str):
    return db.query(models.Producto).filter(models.Producto.codigo_barras == codigo).first()

def obtener_todos(db: Session):
    return db.query(models.Producto).all()

def obtener_stock_bajo(db: Session, limite: int = 5):
    # Buscamos productos donde el stock sea menor al límite
    return db.query(models.Producto).filter(models.Producto.stock_actual < limite).all()

def actualizar_producto(db: Session, producto_id: int, datos_nuevos: schemas.ProductoCreate):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        # Actualizamos cada campo con los nuevos datos
        for key, value in datos_nuevos.model_dump().items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
        return True
    return False

def buscar_productos_por_nombre(db: Session, nombre: str):
    # La lógica es: filtra productos donde el nombre se parezca a lo que escribió el usuario
    return db.query(models.Producto).filter(models.Producto.nombre.ilike(f"%{nombre}%")).all()