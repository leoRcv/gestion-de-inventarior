from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from datetime import datetime

def realizar_venta(db: Session, venta_in: schemas.VentaCreate):
    # 1. Crear la cabecera de la Venta
    nueva_venta = models.Venta(total=0)
    db.add(nueva_venta)
    db.flush() # Para obtener el ID de la venta sin terminar la transacción
    
    total_acumulado = 0
    
    # 2. Procesar cada producto del carrito
    for item in venta_in.detalles:
        producto = db.query(models.Producto).filter(models.Producto.id == item.producto_id).first()
        
        # Validar que el producto exista
        if not producto:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"Producto con ID {item.producto_id} no existe.")

        # Validar Stock: Escudo anti stock negativo
        if producto.stock_actual < item.cantidad:
            # Revertir la operación
            db.rollback()
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para vender {item.cantidad} unidades de '{producto.nombre}'. Solo quedan {producto.stock_actual}.")

        # Calcular subtotal
        subtotal = producto.precio_venta * item.cantidad
        total_acumulado += subtotal
        
        # Crear el detalle
        detalle = models.VentaDetalle(
            venta_id=nueva_venta.id,
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio_venta
        )
        db.add(detalle)
        
        # ACTUALIZAR STOCK
        producto.stock_actual -= item.cantidad
        
        # REGISTRAR MOVIMIENTO DE SALIDA
        mov = models.Movimiento(
            producto_id=producto.id,
            tipo="SALIDA",
            cantidad=item.cantidad,
            motivo=f"Venta #{nueva_venta.id}"
        )
        db.add(mov)

    nueva_venta.total = total_acumulado
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta