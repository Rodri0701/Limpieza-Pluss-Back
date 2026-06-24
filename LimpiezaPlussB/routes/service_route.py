from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import SessionLocal
from ..schemas.service_schema import ServicioCreate, ServicioUpdate, ServicioResponse
from ..services.service_service import (
    crear_servicio,
    obtener_servicios,
    obtener_servicio_por_id,
    actualizar_servicio,
    eliminar_servicio
)

from ..config.dependencies import obtener_usuario_actual, obtener_usuario_admin
from ..models.user_model import Usuarios

# Agregamos el tag para agrupar en Swagger de manera profesional
router = APIRouter(tags=["Servicios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 1. CREAR SERVICIO (Solo Admin)
# ==========================================
@router.post("/servicios/", response_model=ServicioResponse)
def crear(
    servicio_in: ServicioCreate, 
    db: Session = Depends(get_db),
    admin: Usuarios = Depends(obtener_usuario_admin)
):
    print(f"El administrador {admin.nombre} está creando un servicio.")
    # CORRECCIÓN: Pasamos el ID del admin de forma segura extraído del JWT
    return crear_servicio(servicio_in=servicio_in, db=db, admin_id=admin.id_user)

# ==========================================
# 2. OBTENER TODOS LOS SERVICIOS (Público)
# ==========================================
@router.get("/servicios/", response_model=List[ServicioResponse])
def obtener_todos(db: Session = Depends(get_db)):
    return obtener_servicios(db=db)

# ==========================================
# 3. OBTENER UN SERVICIO POR ID (Público)
# ==========================================
@router.get("/servicios/{servicio_id}", response_model=ServicioResponse)
def obtener_uno(servicio_id: int, db: Session = Depends(get_db)): 
    return obtener_servicio_por_id(servicio_id=servicio_id, db=db)

# ==========================================
# 4. ACTUALIZAR SERVICIO (Solo Admin)
# ==========================================
@router.put("/servicios/{servicio_id}", response_model=ServicioResponse)
def actualizar(
    servicio_id: int, 
    servicio_in: ServicioUpdate, 
    db: Session = Depends(get_db), 
    admin: Usuarios = Depends(obtener_usuario_admin)
):
    # CORRECCIÓN: Enviamos el admin_id para saber quién modificó el catálogo
    return actualizar_servicio(servicio_id=servicio_id, servicio_in=servicio_in, db=db, admin_id=admin.id_user)

# ==========================================
# 5. ELIMINAR SERVICIO (Solo Admin - Soft Delete)
# ==========================================
@router.delete("/servicios/{servicio_id}")
def eliminar(
    servicio_id: int, 
    db: Session = Depends(get_db), 
   admin: Usuarios = Depends(obtener_usuario_admin)
):
    # CORRECCIÓN: Enviamos el admin_id para registrar la baja lógica en auditoría
    return eliminar_servicio(servicio_id=servicio_id, db=db, admin_id=admin.id_user)