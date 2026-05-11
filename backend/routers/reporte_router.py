from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import reporte_repo

# 1. IMPORTAMOS AL GUARDIA DE SEGURIDAD
from dependencies import verificar_admin 

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# 2. AGREGAMOS AL GUARDIA EN LA RUTA (dependencies=[Depends(verificar_admin)])
@router.get("/cierre-caja", response_model=schemas.CierreCaja, dependencies=[Depends(verificar_admin)])
def cierre_de_caja(db: Session = Depends(get_db)):
    """
    Obtiene el reporte del día: Total de tickets de venta y dinero recaudado.
    (Protegido: Solo para Administradores)
    """
    return reporte_repo.obtener_cierre_caja_hoy(db)