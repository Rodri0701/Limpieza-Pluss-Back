from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..config.database import SessionLocal
from ..schemas.reserva_schema import ReservaCreate, ReservaResponse
from ..services.reserva_service import crear_reserva, obtener_mis_reservas,reagendar_reserva_empleado,cancelar_reserva_cliente,marcar_como_realizado, asignar_empleado_admin
from ..models.reserva_model import Reserva

# Importamos a los guardias
from ..config.dependencies import obtener_usuario_actual, obtener_usuario_admin,obtener_usuario_empleado
from ..models.user_model import Usuarios

router = APIRouter(tags=["Reservas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 1. CLIENTE: AGENDAR CITA
# ==========================================
@router.post("/reservas/me", response_model=ReservaResponse)
def agendar(
    reserva_in: ReservaCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    return crear_reserva(db=db, reserva_in=reserva_in, user_id=usuario_actual.id_user)

# ==========================================
# 2. CLIENTE: VER MIS CITAS
# ==========================================
@router.get("/reservas/me", response_model=List[ReservaResponse])
def ver_mis_citas(
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    return obtener_mis_reservas(db=db, user_id=usuario_actual.id_user)

# ==========================================
# 3. ADMIN: VER TODA LA AGENDA DEL NEGOCIO
# ==========================================
@router.get("/reservas/todas", response_model=List[ReservaResponse])
def ver_agenda_completa(
    db: Session = Depends(get_db),
    admin: Usuarios = Depends(obtener_usuario_admin) # <-- Guardia de Élite
):
    return db.query(Reserva).all()


# 1. BOTÓN DEL CLIENTE
@router.patch("/reservas/me/{reserva_id}/cancelar", response_model=ReservaResponse)
def cliente_cancela_cita(
    reserva_id: int, 
    db: Session = Depends(get_db),
    cliente: Usuarios = Depends(obtener_usuario_actual) # Cualquier logueado
):
    return cancelar_reserva_cliente(db=db, reserva_id=reserva_id, cliente_id=cliente.id_user)

# 2. BOTÓN DEL EMPLEADO / ADMIN
@router.patch("/reservas/empleado/{reserva_id}/reagendar", response_model=ReservaResponse)
def empleado_reagenda_cita(
    reserva_id: int,
    nueva_fecha: datetime, 
    db: Session = Depends(get_db),
    # Aquí el guardia ya deja pasar tanto a Empleados como Administradores
    usuario_solicitante: Usuarios = Depends(obtener_usuario_empleado) 
):
    # Le pasamos el objeto completo del usuario en lugar de solo su ID
    return reagendar_reserva_empleado(
        db=db, 
        reserva_id=reserva_id, 
        usuario_solicitante=usuario_solicitante, 
        nueva_fecha=nueva_fecha
    )

# 3. BOTONES DEL ADMIN
@router.patch("/reservas/admin/{reserva_id}/asignar/{empleado_id}", response_model=ReservaResponse)
def admin_asigna_empleado(
    reserva_id: int,
    empleado_id: int,
    db: Session = Depends(get_db),
    admin: Usuarios = Depends(obtener_usuario_admin) # Guardia Nivel 3
):
    return asignar_empleado_admin(db=db, reserva_id=reserva_id, empleado_id=empleado_id)

# 4. BOTÓN DE EMPLEADO Y ADMIN (Cerrar el trabajo)
@router.patch("/reservas/empleado/{reserva_id}/realizado", response_model=ReservaResponse)
def marcar_realizado(
    reserva_id: int,
    db: Session = Depends(get_db),
    # Este guardia permite pasar al Empleado y al Admin
    usuario_solicitante: Usuarios = Depends(obtener_usuario_empleado) 
):
    return marcar_como_realizado(db=db, reserva_id=reserva_id, usuario_solicitante=usuario_solicitante)