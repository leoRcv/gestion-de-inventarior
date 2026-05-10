# repositories/movimiento_repo.py
from sqlalchemy.orm import Session
from models import models

def obtener_movimientos_por_producto(db: Session, producto_id: int):
    # Lógica: Traer historial del producto X, ordenado por fecha descendente
    return db.query(models.Movimiento)\
             .filter(models.Movimiento.producto_id == producto_id)\
             .order_by(models.Movimiento.fecha.desc())\
             .all()