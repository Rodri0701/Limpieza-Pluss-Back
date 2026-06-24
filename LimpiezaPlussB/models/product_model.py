from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.sql import func # IMPORTANTE: Para que la base de datos ponga la fecha exacta
from ..config.database import Base

class Producto(Base):
    __tablename__ = "productos" 
    
    # Estandarizamos todo a minúsculas (snake_case)
    id_producto = Column(Integer, primary_key=True, index=True) 
    nombre_producto = Column(String(100), unique=True, nullable=False) 
    precio = Column(Numeric(10,2), nullable=False) 
    descripcion = Column(String(500), nullable=False) 
    categoria = Column(String(100), nullable=False) 
    stock = Column(Integer, nullable=False) 
    descuento = Column(Integer, nullable=False)
    
    # NUEVO: Estatus para el Borrado Lógico ("A" = Activo, "I" = Inactivo)
    status = Column(String(1), default="A", nullable=False)
    
    # CORRECCIÓN: func.now() asegura que se guarde la fecha del momento exacto
    fecha_creacion = Column(DateTime, default=func.now())
    
    # Estas columnas guardarán el ID (int) del Administrador que hizo la acción
    user_alta = Column(Integer, nullable=True) 
    user_update = Column(Integer, nullable=True)
    fecha_update = Column(DateTime, nullable=True, onupdate=func.now()) # Se actualiza sola al editar