from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import producto_repo

router = APIRouter(prefix="/productos", tags=["Productos"])

# 1. RUTA DE CREACIÓN (POST)
@router.post("/", response_model=schemas.Producto)
def crear(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return producto_repo.crear_producto(db, producto)

# 2. RUTAS ESTÁTICAS (Deben ir ARRIBA de las que tienen variables)
# Esta ruta se activa con: GET /productos/reporte/stock-bajo
@router.get("/reporte/stock-bajo", response_model=list[schemas.ReporteStock])
def reporte_inventario(db: Session = Depends(get_db)):
    productos = producto_repo.obtener_stock_bajo(db)
    
    reporte = []
    for p in productos:
        estado = "AGOTADO" if p.stock_actual == 0 else "BAJO"
        reporte.append(schemas.ReporteStock(
            nombre=p.nombre, 
            stock_actual=p.stock_actual, 
            estado=estado
        ))
    
    return reporte

# 3. RUTAS CON VARIABLES (Parámetros de ruta)
# Se pone al final porque /{codigo} es un "comodín" que atrapa cualquier texto
@router.get("/{codigo}", response_model=schemas.Producto)
def buscar_por_codigo(codigo: str, db: Session = Depends(get_db)):
    db_producto = producto_repo.obtener_por_codigo(db, codigo)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/{producto_id}", response_model=schemas.Producto)
def actualizar(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    res = producto_repo.actualizar_producto(db, producto_id, producto)
    if not res:
        raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar")
    return res

@router.delete("/{producto_id}")
def eliminar(producto_id: int, db: Session = Depends(get_db)):
    exito = producto_repo.eliminar_producto(db, producto_id)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: Producto inexistente")
    return {"message": "Producto eliminado correctamente"}

@router.get("/buscar/nombre", response_model=list[schemas.Producto])
def buscar_nombre(nombre: str, db: Session = Depends(get_db)):
    productos = producto_repo.buscar_productos_por_nombre(db, nombre)
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos con ese nombre")
    return productos

@router.get("/{producto_id}/movimientos", response_model=list[schemas.Movimiento])
def ver_historial(producto_id: int, db: Session = Depends(get_db)):
    return producto_repo.obtener_historial_movimientos(db, producto_id)

@router.get("/", response_model=list[schemas.Producto])
def listar_todos(db: Session = Depends(get_db)):
    # Usamos el repositorio para traer absolutamente todos los productos
    return producto_repo.obtener_todos(db) 
    # Nota: Asegúrate de que 'obtener_todos_los_productos' o similar exista en tu 'producto_repo'

@router.post("/{producto_id}/ajustar")
def ajustar_stock(producto_id: int, ajuste: schemas.AjusteStock, db: Session = Depends(get_db)):
    producto = producto_repo.ajustar_stock_manual(db, producto_id=producto_id, ajuste=ajuste)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto