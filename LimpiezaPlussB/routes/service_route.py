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

from..config.dependencies import obtener_usuario_actual, obtener_usuario_admin
from ..models.user_model import Usuarios

router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CREAR SERVICIO
@router.post("/servicios/", response_model=ServicioResponse)
def crear(servicio_in: ServicioCreate, db: Session = Depends(get_db),
        admin: Usuarios = Depends(obtener_usuario_admin)):
    print(f"El usuario {admin.nombre} está creando un servicio.")
    return crear_servicio(servicio_in=servicio_in, db=db)

# 2. OBTENER TODOS LOS SERVICIOS
# Nota: Usamos List[ServicioResponse] porque devolveremos un arreglo de objetos
@router.get("/servicios/", response_model=List[ServicioResponse])
def obtener_todos(db: Session = Depends(get_db)):
    
    return obtener_servicios(db=db)

# 3. OBTENER UN SERVICIO POR ID
@router.get("/servicios/{servicio_id}", response_model=ServicioResponse)
def obtener_uno(servicio_id: int, db: Session = Depends(get_db)): 
    return obtener_servicio_por_id(servicio_id=servicio_id, db=db)

# 4. ACTUALIZAR SERVICIO
@router.put("/servicios/{servicio_id}", response_model=ServicioResponse)
def actualizar(servicio_id: int, servicio_in: ServicioUpdate, db: Session = Depends(get_db), admin: Usuarios = Depends(obtener_usuario_admin)):
    return actualizar_servicio(servicio_id=servicio_id, servicio_in=servicio_in, db=db)

# 5. ELIMINAR SERVICIO (Inactivar)
@router.delete("/servicios/{servicio_id}")
def eliminar(servicio_id: int, db: Session = Depends(get_db), admin: Usuarios = Depends(obtener_usuario_admin)):
    return eliminar_servicio(servicio_id=servicio_id, db=db)