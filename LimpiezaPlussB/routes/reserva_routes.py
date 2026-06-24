from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import SessionLocal
from ..schemas.reserva_schema import ReservaCreate, ReservaResponse
from ..services.reserva_service import crear_reserva, obtener_mis_reservas
from ..models.reserva_model import Reserva

# Importamos a los guardias
from ..config.dependencies import obtener_usuario_actual, obtener_usuario_admin
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