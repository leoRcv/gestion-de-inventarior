# routers/movimiento_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import movimiento_repo

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])

@router.get("/{producto_id}", response_model=list[schemas.Movimiento])
def leer_historial(producto_id: int, db: Session = Depends(get_db)):
    return movimiento_repo.obtener_movimientos_por_producto(db, producto_id)