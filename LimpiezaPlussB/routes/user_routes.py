from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user_model import Usuarios
from ..schemas.user_schema import UsuarioCreate, UsuarioResponse  # Tus schemas de Pydantic
from ..config.security import get_password_hash  # La función que creamos al inicio
from ..config.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
        
@router.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_pwd = get_password_hash(usuario_in.password)
    datos_usuario = usuario_in.model_dump(exclude={"password"}) 
    nuevo_usuario = Usuarios(**datos_usuario, hashed_password=hashed_pwd)
    
    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        db.rollback() # Deshace el cambio fallido
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")