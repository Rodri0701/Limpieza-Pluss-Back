from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from ..config.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva = Column(Integer, primary_key=True, index=True)
    
    # ¿Quién reserva y qué servicio?
    user_id = Column(Integer, ForeignKey("usuarios.id_user"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id_servicio"), nullable=False)
    
    # ¿Cuándo es la cita?
    fecha_reserva = Column(DateTime, nullable=False)
    
    # Estatus de la cita ("Pendiente", "Confirmada", "Cancelada")
    status = Column(String(20), default="Pendiente")
    
    # Auditoría: ¿Cuándo hizo clic en "Reservar"?
    fecha_creacion = Column(DateTime, default=func.now())