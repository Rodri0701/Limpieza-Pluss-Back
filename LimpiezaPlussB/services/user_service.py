from sqlalchemy.orm import Session
from ..models.user_model import Usuarios
from ..schemas.user_schema import UsuarioCreate, UsuarioUpdate
from fastapi import HTTPException
from ..config.security import get_password_hash 
from sqlalchemy.exc import IntegrityError

def crear_usuario(usuario_in: UsuarioCreate, db: Session):
    hashed_pwd = get_password_hash(usuario_in.password)
    datos_usuario = usuario_in.model_dump(exclude={"password"}) 
    nuevo_usuario = Usuarios(**datos_usuario, hashed_password=hashed_pwd)
    
    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    

def view_usuario(usuario_id: int, db: Session):

    usuario = db.query(Usuarios).filter(Usuarios.id_user == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

def actualizar_usuario(db: Session, usuario_id: int, usuario_in: UsuarioUpdate):
    usuario_db = db.query(Usuarios).filter(Usuarios.id_user == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 1. Convertimos el esquema a diccionario ignorando los campos que el usuario NO mandó
    datos_a_actualizar = usuario_in.model_dump(exclude_unset=True)

    # 2. TRATAMIENTO QUIRÚRGICO PARA LA CONTRASEÑA (El Blindaje)
    if "password" in datos_a_actualizar:
        pass_nuevo = datos_a_actualizar["password"]
        
        # Si el password nuevo es válido (no está vacío y no es el texto por defecto de Swagger)
        if pass_nuevo and pass_nuevo.strip() != "" and pass_nuevo.lower() != "string":
            # Lo encriptamos antes de guardarlo en la columna hashed_password
            usuario_db.hashed_password = get_password_hash(pass_nuevo)
            
        # Sacamos el password del diccionario para que el bucle de abajo no intente mapearlo ciegamente
        datos_a_actualizar.pop("password")

    # 3. Bucle para actualizar el resto de los campos normales (nombre, edad, etc.)
    for llave, valor in datos_a_actualizar.items():
        setattr(usuario_db, llave, valor)

    db.commit()
    db.refresh(usuario_db)
    
    return usuario_db


def eliminar_usuario(db:Session, id_usuario: int):
    
    usuario = db.query(Usuarios).filter(
        Usuarios.id_user == id_usuario
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail= "error al eliminar"
        )
    
    db.delete(usuario)
    db.commit()
    
def obtener_todos_los_usuarios(db: Session):
    return db.query(Usuarios).all()