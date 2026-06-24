from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from ..models.service_model import Servicio
from ..schemas.service_schema import ServicioCreate, ServicioUpdate

# ==========================================
# 1. CREAR
# ==========================================
def crear_servicio(servicio_in: ServicioCreate, db: Session, admin_id: int):
    # Verificamos que el nombre no exista previamente (ignorando mayúsculas/minúsculas)
    servicio_existente = db.query(Servicio).filter(
        func.lower(Servicio.nombre_servicio) == servicio_in.nombre_servicio.lower()
    ).first()
    
    if servicio_existente:
        raise HTTPException(status_code=400, detail=f"El servicio '{servicio_in.nombre_servicio}' ya está registrado.")
    
    # Creamos el servicio asignando al Admin responsable
    datos_servicio = servicio_in.model_dump() 
    nuevo_servicio = Servicio(
        **datos_servicio, 
        user_alta=admin_id 
        # No mandamos fecha_creacion, la BD lo hace sola con func.now()
    )
    
    try:
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        return nuevo_servicio
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=500, detail="Error interno al guardar en la base de datos.")

# ==========================================
# 2. LEER
# ==========================================
def obtener_servicios(db: Session):
    # Solo mostramos los activos
    return db.query(Servicio).filter(Servicio.status == "A").all()

def obtener_servicio_por_id(servicio_id: int, db: Session):
    # Solo permitimos ver si está activo
    servicio = db.query(Servicio).filter(
        Servicio.id_servicio == servicio_id,
        Servicio.status == "A"
    ).first()
    
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o descontinuado")
    return servicio

# ==========================================
# 3. ACTUALIZAR
# ==========================================
def actualizar_servicio(servicio_id: int, servicio_in: ServicioUpdate, db: Session, admin_id: int):
    servicio_db = obtener_servicio_por_id(servicio_id, db)
    datos_a_actualizar = servicio_in.model_dump(exclude_unset=True)
    
    if "nombre_servicio" in datos_a_actualizar:
        nuevo_nombre = datos_a_actualizar["nombre_servicio"]
        nombre_ocupado = db.query(Servicio).filter(
            func.lower(Servicio.nombre_servicio) == nuevo_nombre.lower(), 
            Servicio.id_servicio != servicio_id
        ).first()
        if nombre_ocupado:
            raise HTTPException(status_code=400, detail="Ese nombre ya está en uso por otro servicio.")
    
    for llave, valor in datos_a_actualizar.items():
        setattr(servicio_db, llave, valor)
        
    # Registramos qué Admin hizo el cambio
    servicio_db.user_update = admin_id
        
    try:
        db.commit()
        db.refresh(servicio_db)
        return servicio_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar la base de datos.")

# ==========================================
# 4. ELIMINAR (Soft Delete)
# ==========================================
def eliminar_servicio(servicio_id: int, db: Session, admin_id: int):
    # Usamos nuestra propia función de búsqueda que ya valida que exista y esté activo
    servicio_db = obtener_servicio_por_id(servicio_id, db)
        
    # Cambiamos el estatus y registramos quién lo borró
    servicio_db.status = "I"
    servicio_db.user_update = admin_id
    
    db.commit()
    
    return {"mensaje": f"El servicio '{servicio_db.nombre_servicio}' ha sido eliminado del catálogo."}