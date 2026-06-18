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

def actualizar_usuario(usuario_id: int, db: Session, usuario_in: UsuarioUpdate  ):
    # 2. Buscar si el usuario existe en la Base de Datos
    usuario_db = db.query(Usuarios).filter(Usuarios.id_user == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 3. Extraer los datos del esquema, ignorando los que vengan como None (exclude_unset=True)
    datos_a_actualizar = usuario_in.model_dump(exclude_unset=True)
    
    # 4. Caso especial: Si el usuario envió una nueva contraseña, hay que encriptarla
    if "password" in datos_a_actualizar:
        nueva_pwd_plana = datos_a_actualizar.pop("password") # Sacamos la contraseña en texto plano
        datos_a_actualizar["hashed_password"] = get_password_hash(nueva_pwd_plana) # Metemos el hash
        
    # 5. Mapear dinámicamente los campos que sí se enviaron hacia el objeto de SQLAlchemy
    for llave, valor in datos_a_actualizar.items():
        setattr(usuario_db, llave, valor)
        
    # 6. Guardar los cambios en la base de datos
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
    