from sqlalchemy import Column, Integer, String, Numeric, DateTime, Float
from sqlalchemy.sql import func
from ..config.database import Base 

class Servicio(Base):
    __tablename__ = "servicios" 
    
    # Estandarizado a snake_case
    id_servicio = Column(Integer, primary_key=True, index=True) 
    nombre_servicio = Column(String(100), unique=True, nullable=False) 
    precio = Column(Numeric(10, 2), nullable=False) 
    descripcion = Column(String(500), nullable=False) 
    categoria = Column(String(100), nullable=False) 
    duracion_estimada_horas = Column(Float, nullable=True)
    
    # Estatus estándar para Soft Delete ("A" = Activo, "I" = Inactivo)
    status = Column(String(1), default="A", nullable=False) 
    
    # Auditoría (Creación y Edición por el Admin)
    fecha_creacion = Column(DateTime, default=func.now()) 
    user_alta = Column(Integer, nullable=True) # ID del Admin que lo creó
    user_update = Column(Integer, nullable=True) # ID del Admin que lo editó
    fecha_update = Column(DateTime, nullable=True, onupdate=func.now()) # Se actualiza sola