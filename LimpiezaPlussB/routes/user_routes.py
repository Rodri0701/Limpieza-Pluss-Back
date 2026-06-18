from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.user_service import crear_usuario, view_usuario, actualizar_usuario,eliminar_usuario
from ..schemas.user_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from ..config.database import SessionLocal

router = APIRouter()

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
@router.get("/vista_user/{usuario_id}", response_model=UsuarioResponse) 
def ver (usuario_id: int, db: Session = Depends(get_db)):
    return view_usuario(usuario_id,db)


# #RUTA PARA ACTUALIZAR SUS DATOS
@router.put("/usuario/{usuario_id}", response_model=UsuarioResponse)
def actualizar(
    usuario_id: int, 
    usuario_in: UsuarioUpdate, # 1. Le pedimos a FastAPI que reciba el JSON del cliente
    db: Session = Depends(get_db)
):
    # 2. Le pasamos los 3 datos completos a tu servicio
    actualizar_usuario(
        usuario_id=usuario_id, 
        db=db, 
        usuario_in=usuario_in
    )
    
    return ("Se actualizó de forma exitosa")

# #RUTA PARA ELIMINAR AL USUARIO
@router.delete("/usuario/{usuario_id}")
def delete_user(
  usuario_id : int,
  db: Session = Depends(get_db)  
):
    eliminar_usuario(db,usuario_id)
    return ( "Eliminado exitosamente")