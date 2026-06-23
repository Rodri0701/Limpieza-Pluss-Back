from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.user_service import crear_usuario, obtener_todos_los_usuarios, actualizar_usuario,eliminar_usuario
from ..schemas.user_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from ..config.database import SessionLocal

from ..config.dependencies import obtener_usuario_actual, obtener_usuario_admin
from ..models.user_model import Usuarios
from typing import List

router = APIRouter(tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
#RUTA PARA CREAR LOS USUARIOS        
@router.post("/usuarios/", response_model=UsuarioResponse) 
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
     return crear_usuario(usuario_in=usuario, db=db)
    

#RUTA PARA QUE EL USUARIO EN SESION PUEDA VER SOLO SU INFORMACION
@router.get("/usuarios/me", response_model= UsuarioResponse)
def ver_mi_perfil(usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    return usuario_actual


# #RUTA PARA ACTUALIZAR SUS DATOS
@router.put("/usuarios/me", response_model=UsuarioResponse)
def actualziar_mi_perfil( datos_actualizar: UsuarioUpdate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    return actualizar_usuario(db=db, usuario_id= usuario_actual.id_user, usuario_in= datos_actualizar)

# #RUTA PARA ELIMINAR AL USUARIO
@router.delete("/usuarios/me")
def eliminar_mi_cuenta(
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    return eliminar_usuario(db=db, usuario_id= usuario_actual.id_user)


# RUTA UNICA PARA EL ADMINISTRADOR
@router.get("/usuarios/todos", response_model=List[UsuarioResponse])
def ver_todos_los_usuarios( db: Session = Depends(get_db),  admin: Usuarios = Depends(obtener_usuario_admin)
):
    return obtener_todos_los_usuarios (db=db)