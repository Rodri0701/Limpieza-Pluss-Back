from sqlalchemy import Column, Integer, String, Numeric, DateTime, Float, ForeignKey
from sqlalchemy.sql import func  # Para manejar la fecha automática de creación
from ..config.database import Base 

#TABLAS PARA CREAR  LA TABLA EN LA BASE DE DATOS DESDE PYTHON
class Servicio(Base):
    __tablename__ = "servicios" 
    
    id_Servicio = Column(Integer, primary_key=True, index=True) #ID PRINCIPAL
    nombre_Servicio = Column(String(100), unique=True, nullable=False) #NOMBRE DEL SERVICIO
    precio = Column(Numeric(10, 2), nullable=False) #PRECIO
    Descripcion = Column(String(500), nullable=False) #DESCRIPCION
    Categoria = Column(String(100), nullable=False) #CATEGORIA
    Status_servicio = Column(String(1), default="A") #STATUS DEL MISMO 
    # A = ACTIVO
    # O = OCUPADO
    # I = INACTIVO
    
    # Control de reservas
    fecha_reserva = Column(DateTime, nullable=True) 
    
    # RELACION FORANEA
    user_id = Column(Integer, ForeignKey("usuarios.id_user"), nullable=True)
    
    # Auditoría (Creación y Edición)
    fecha_creacion = Column(DateTime, default=func.now()) # Usa la hora del servidor de BD automáticamente
    duracion_estimada_horas = Column(Float, nullable=True)
    user_alta = Column(String(50), nullable=True) 
    user_update = Column(String(50), nullable=True)
    fecha_update = Column(DateTime, nullable=True)