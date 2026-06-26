from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from ..models.reserva_model import Reserva
from ..models.service_model import Servicio
from ..schemas.reserva_schema import ReservaCreate
from ..models.user_model import Usuarios

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

# ==========================================
# REGLA 1: CLIENTE CANCELA
# ==========================================
def cancelar_reserva_cliente(db: Session, reserva_id: int, cliente_id: int):
    reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id, Reserva.user_id == cliente_id).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
        
    # Solo puede cancelar si la cita no ha sucedido ni ha sido cancelada antes
    if reserva.status not in ["Pendiente", "Reagendada"]:
        raise HTTPException(status_code=400, detail=f"No puedes cancelar una reserva que está {reserva.status}.")
        
    reserva.status = "Cancelada"
    db.commit()
    db.refresh(reserva)
    return reserva

# ==========================================
# REGLA 2 EMPLEADO/ADMIN REAGENDA
# ==========================================
# Ahora recibimos todo el objeto del usuario solicitante, no solo su ID
def reagendar_reserva_empleado(db: Session, reserva_id: int, usuario_solicitante, nueva_fecha: datetime):
    # 1. Buscamos la reserva sin importar a quién esté asignada todavía
    reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    
    # 2. EL BLINDAJE: Verificamos si tiene permiso de tocarla
    # Si NO es Admin Y TAMPOCO es el empleado asignado a esta cita... ¡Bloqueado!
    if usuario_solicitante.roll != "admin" and reserva.empleado_id != usuario_solicitante.id_user:
        raise HTTPException(status_code=403, detail="No puedes reagendar una reserva que no te ha sido asignada.")
        
    if reserva.status in ["Realizado", "Cancelada"]:
        raise HTTPException(status_code=400, detail="No se puede reagendar una cita finalizada o cancelada.")
        
    # Quitamos la zona horaria y actualizamos
    reserva.fecha_reserva = nueva_fecha.replace(tzinfo=None)
    reserva.status = "Reagendada"
    
    db.commit()
    db.refresh(reserva)
    return reserva

# ==========================================
# REGLA 3 CORREGIDA: ADMIN ASIGNA
# ==========================================
def asignar_empleado_admin(db: Session, reserva_id: int, empleado_id: int):
    # 1. EL BLINDAJE: Verificamos que el usuario al que le queremos asignar exista Y SEA EMPLEADO
    empleado_db = db.query(Usuarios).filter(Usuarios.id_user == empleado_id).first()
    
    if not empleado_db:
        raise HTTPException(status_code=404, detail="El ID de usuario proporcionado no existe.")
        
    if empleado_db.roll not in ["Empleado", "admin"]:
        raise HTTPException(status_code=400, detail="No puedes asignar un servicio a un usuario normal. Debe tener rol de Empleado.")

    # 2. Ahora sí, buscamos la reserva y la asignamos
    reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
        
    reserva.empleado_id = empleado_id
    db.commit()
    db.refresh(reserva)
    return reserva
# ==========================================
# REGLA 4: MARCAR COMO REALIZADO (Empleado/Admin)
# ==========================================
def marcar_como_realizado(db: Session, reserva_id: int, usuario_solicitante):
    reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    
    if usuario_solicitante.roll != "Admin" and reserva.empleado_id != usuario_solicitante.id_user:
        raise HTTPException(
            status_code=403, 
            detail="No puedes marcar como realizada una reserva que no te ha sido asignada."
        )
        
    # Evitamos re-procesar algo ya terminado
    if reserva.status in ["Realizado", "Cancelada"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Operación inválida. La reserva actualmente está: {reserva.status}"
        )
        
    reserva.status = "Realizado"
    db.commit()
    db.refresh(reserva)
    
    return reserva