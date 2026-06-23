from fastapi import APIRouter, Depends, Response,status
from sqlalchemy.orm import Session

from ..schemas.product_schema import ProductoCreate, ProductoUpdate
from ..services.product_service import crear_producto, obtener_producto,obtener_productos, actualizar_producto, eliminar_producto
from ..config.database import SessionLocal
from ..models.user_model import Usuarios
from ..config.dependencies import obtener_usuario_actual, obtener_usuario_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

#FUNCION PARA INSERTAR PRODUCTOS CON SU RUTA

@router.post("/productos")
def crear(producto: ProductoCreate, db: Session = Depends(get_db), admin: Usuarios = Depends(obtener_usuario_admin)):
    print(f"El usuario {admin.nombre} esta creando un producto.")
    return crear_producto(db, producto)

# RUTA PARA VER LOS PRODUCTOS POR ID
@router.get("/view-productos/{id_producto}")
def view_producto(id_producto: int, db: Session = Depends(get_db)):
    return obtener_producto(db, id_producto)

# RUTA PARA TODOS LOS PRODUCTOS
@router.get("/view-productos")
def view_productos(db: Session = Depends(get_db)):
    return obtener_productos(db)

#ACTUAZIZAR PRODUCTOS

@router.put("/productos/{id_producto}")
def actualizar(
    id_producto: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),admin: Usuarios = Depends(obtener_usuario_admin)
):
    return actualizar_producto(db, id_producto, producto)


#RUTA PARA ELIMINAR UN PRODUCTO
@router.delete("/productos/{id_producto}")
def delete_producto(
    id_producto: int,
    db: Session = Depends(get_db),admin: Usuarios = Depends(obtener_usuario_admin)
):
    return eliminar_producto(db, id_producto)