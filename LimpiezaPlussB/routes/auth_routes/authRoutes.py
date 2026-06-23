from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...config.database import SessionLocal
from ...models.user_model import Usuarios
from ...config.security import verify_password, crear_token_acceso

from ...schemas.user_schema import LoginRequest

router = APIRouter(tags=["Autenticación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(credenciales: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuarios).filter(Usuarios.email == credenciales.username).first()
    
    if not usuario_db or not verify_password(credenciales.password, usuario_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    datos_token = {"sub": str(usuario_db.id_user)}
    token = crear_token_acceso(datos_token)
    
    return {"access_token": token, "token_type": "bearer"}