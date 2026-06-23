from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ..models.service_model import Servicio
from ..schemas.service_schema import ServicioCreate, ServicioUpdate

# 1. CREAR

def crear_servicio(servicio_in: ServicioCreate, db: Session):
    # Verificamos que el nombre no exista previamente
    servicio_existente = db.query(Servicio).filter(Servicio.nombre_Servicio == servicio_in.nombre_Servicio).first()
    if servicio_existente:
        raise HTTPException(status_code=400, detail=f"El servicio '{servicio_in.nombre_Servicio}' ya está registrado.")
    
    datos_servicio = servicio_in.model_dump() 
    nuevo_servicio = Servicio(**datos_servicio, user_alta="SISTEMA", user_update=None, fecha_creacion= datetime.now())
    
    try:
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        return nuevo_servicio
    except IntegrityError:
        # Si por alguna razón de red o concurrencia falla la base de datos, deshacemos el cambio
        db.rollback() 
        raise HTTPException(status_code=500, detail="Error interno al guardar en la base de datos.")

# 2. LEER

def obtener_servicios(db: Session):
    
   return db.query(Servicio).filter(Servicio.Status_servicio == "A").all()

# LEER POR ID
def obtener_servicio_por_id(servicio_id: int, db: Session):
    servicio = db.query(Servicio).filter(Servicio.id_Servicio == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


# 3. ACTUALIZAR

def actualizar_servicio(servicio_id: int, servicio_in: ServicioUpdate, db: Session):
    servicio_db = obtener_servicio_por_id(servicio_id, db)
    datos_a_actualizar = servicio_in.model_dump(exclude_unset=True)
    
    if "nombre_Servicio" in datos_a_actualizar:
        nuevo_nombre = datos_a_actualizar["nombre_Servicio"]
        nombre_ocupado = db.query(Servicio).filter(
            Servicio.nombre_Servicio == nuevo_nombre, 
            Servicio.id_Servicio != servicio_id
        ).first()
        if nombre_ocupado:
            raise HTTPException(status_code=400, detail="Ese nombre ya está en uso por otro servicio.")
    
    for llave, valor in datos_a_actualizar.items():
        setattr(servicio_db, llave, valor)
        
    try:
        db.commit()
        db.refresh(servicio_db)
        return servicio_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar la base de datos.")

# 4. ELIMINAR 

def eliminar_servicio(servicio_id: int, db: Session):
    servicio_db = obtener_servicio_por_id(servicio_id, db)
    if servicio_db.Status_servicio == "I":
        raise HTTPException(status_code=400, detail="El servicio ya se encuentra inactivo.")
        
    servicio_db.Status_servicio = "I"
    
    db.commit()
    db.refresh(servicio_db)
    
    return {"mensaje": f"El servicio '{servicio_db.nombre_Servicio}' ha sido marcado como Inactivo de forma segura."}