from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import venta_repo
from models import models

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/", response_model=schemas.Venta)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # realizar_venta lanzará un HTTPException si no hay stock
    resultado = venta_repo.realizar_venta(db, venta)
    return resultado

# Añade esto a routers/venta_router.py

@router.get("/", response_model=list[schemas.Venta])
def obtener_historial_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()