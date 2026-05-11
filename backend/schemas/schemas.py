from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ==========================================
# --- SCHEMAS PARA CATEGORÍAS ---
# ==========================================

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMAS PARA PRODUCTOS ---
# ==========================================

class ProductoBase(BaseModel):
    nombre: str
    codigo_barras: str
    precio_venta: float
    stock_actual: int
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMAS PARA MOVIMIENTOS (Kardex) ---
# ==========================================

class MovimientoBase(BaseModel):
    producto_id: int
    tipo: str  # "ENTRADA" o "SALIDA"
    cantidad: int
    motivo: str

class Movimiento(MovimientoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMAS PARA VENTAS (Maestro-Detalle) ---
# ==========================================

# 1. El detalle (lo que va dentro del carrito)
class VentaDetalleBase(BaseModel):
    producto_id: int
    cantidad: int

class VentaDetalleCreate(VentaDetalleBase):
    pass

class VentaDetalle(VentaDetalleBase):
    id: int
    venta_id: int
    precio_unitario: float

    class Config:
        from_attributes = True

# 2. La venta (el ticket completo)
class VentaCreate(BaseModel):
    # Lógica: Enviamos una lista de productos
    detalles: List[VentaDetalleCreate]

class Venta(BaseModel):
    id: int
    fecha: datetime
    total: float
    # Lógica: La respuesta incluye la lista de lo que se vendió
    detalles: List[VentaDetalle]

    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMAS PARA USUARIOS ---
# ==========================================

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: str = "vendedor" # Puede ser "admin" o "vendedor"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# ==========================================
# --- SCHEMAS PARA LA AUTENTICACIÓN (LOGIN) ---
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ==========================================
# --- SCHEMAS PARA REPORTES ---
# ==========================================

class CierreCaja(BaseModel):
    fecha: str
    ventas_totales: int
    total_recaudado: float

class ReporteStock(BaseModel):
    nombre: str
    stock_actual: int
    estado: str # "OK", "BAJO" o "AGOTADO"

    class Config:
        from_attributes = True