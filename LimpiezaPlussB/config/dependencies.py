from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from .security import SECRET_KEY, ALGORITHM
from .database import SessionLocal # Asegúrate de que apunte a tu SessionLocal real
from ..models.user_model import Usuarios

# Definimos que la ruta para conseguir el token será "/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise excepcion_credenciales
    except jwt.PyJWTError:
        raise excepcion_credenciales
        
    usuario = db.query(Usuarios).filter(Usuarios.id_user == int(user_id)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    return usuario

def obtener_usuario_admin(usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    
    if usuario_actual.roll != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Necesitas ser ADMINISTRADOR para realizar esta acción"
        )
    return usuario_actual


def obtener_usuario_empleado(usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    if usuario_actual.roll not in ["Empleado", "admin"]:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Necesitas permiso de ADMINISTRADOR"
        )
    return usuario_actual