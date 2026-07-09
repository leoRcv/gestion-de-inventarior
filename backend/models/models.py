from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    rol = Column(String, default="vendedor")
    is_active = Column(Boolean, default=True)

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    # Lógica: Una categoría tiene muchos productos
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    codigo_barras = Column(String, unique=True, index=True)
    precio_venta = Column(Float)
    stock_actual = Column(Integer)
    
    # Lógica: El vínculo con la tabla categorias
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    # Esto nos permite acceder a la info de la categoría desde el producto
    categoria = relationship("Categoria", back_populates="productos")
    activo = Column(Boolean, default=True)

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, server_default=func.now())
    total = Column(Float, default=0.0)
    
    # Relación: Una venta tiene muchos detalles
    detalles = relationship("VentaDetalle", back_populates="venta")

class VentaDetalle(Base):
    __tablename__ = "venta_detalles"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float) # Importante: guardar el precio de ese momento

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        if self.precio_unitario is not None and self.cantidad is not None:
            return self.precio_unitario * self.cantidad
        return 0.0

class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tipo = Column(String)  # "ENTRADA" (Compra) o "SALIDA" (Venta)
    cantidad = Column(Integer)
    motivo = Column(String) # Ejemplo: "Venta de producto"
    fecha = Column(DateTime, server_default=func.now()) # Fecha automática
