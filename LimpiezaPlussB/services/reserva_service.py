from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from ..models.reserva_model import Reserva
from ..models.service_model import Servicio
from ..schemas.reserva_schema import ReservaCreate

def crear_reserva(db: Session, reserva_in: ReservaCreate, user_id: int):
    fecha_ingenua = reserva_in.fecha_reserva.replace(tzinfo=None)
    
    # 1. Validar que la fecha no sea en el pasado
    if fecha_ingenua < datetime.now():
        raise HTTPException(status_code=400, detail="No puedes reservar en una fecha pasada.")

    reserva_in.fecha_reserva = fecha_ingenua
    # 2. Validar que el servicio exista y esté activo
    servicio = db.query(Servicio).filter(Servicio.id_servicio == reserva_in.servicio_id).first()
    if not servicio or servicio.status != "A":
        raise HTTPException(status_code=404, detail="El servicio no existe o no está disponible.")

    # 3. Validar disponibilidad (Nadie más tiene ese servicio a esa misma hora)
    # Nota: En un sistema más complejo, validarías rangos de horas (ej. si dura 2 horas).
    choque_horario = db.query(Reserva).filter(
        Reserva.servicio_id == reserva_in.servicio_id,
        Reserva.fecha_reserva == reserva_in.fecha_reserva,
        Reserva.status != "Cancelada"
    ).first()
    
    if choque_horario:
        raise HTTPException(status_code=400, detail="Ese horario ya está ocupado para este servicio.")

    # 4. Crear la reserva
    nueva_reserva = Reserva(
        user_id=user_id,
        servicio_id=reserva_in.servicio_id,
        fecha_reserva=reserva_in.fecha_reserva
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    
    return nueva_reserva

def obtener_mis_reservas(db: Session, user_id: int):
    return db.query(Reserva).filter(Reserva.user_id == user_id).all()