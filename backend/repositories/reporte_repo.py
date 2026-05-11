from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from datetime import date
from models import models

def obtener_cierre_caja_hoy(db: Session):
    hoy = date.today()
    # Buscamos todas las ventas cuya fecha coincida con hoy
    ventas_hoy = db.query(models.Venta).filter(cast(models.Venta.fecha, Date) == hoy).all()
    
    total_recaudado = sum(venta.total for venta in ventas_hoy)
    ventas_totales = len(ventas_hoy)
    
    return {
        "fecha": str(hoy),
        "ventas_totales": ventas_totales,
        "total_recaudado": total_recaudado
    }
