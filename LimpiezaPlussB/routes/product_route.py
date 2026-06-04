from fastapi import APIRouter, Depends, Response,status
from sqlalchemy.orm import Session

from ..schemas.product_schema import ProductoCreate
from ..services.product_service import crear_producto, obtener_producto,obtener_productos, actualizar_producto, eliminar_producto
from ..config.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

#FUNCION PARA INSERTAR PRODUCTOS CON SU RUTA
#FALTA PROTEGERLA

@router.post("/productos")
def crear(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, producto)

# RUTA PARA VERE LOS PRODUCTOS POR ID
@router.get("/view-productos/{id_producto}")
def view_producto(id_producto: int, db: Session = Depends(get_db)):
    return obtener_producto(db, id_producto)

# RUTA PAR TODOS LOS PRODUCTOS
@router.get("/view-productos")
def view_productos(db: Session = Depends(get_db)):
    return obtener_productos(db)

#ACTUAZIZAR PRODUCTOS

@router.put("/productos/{id_producto}")
def actualizar(
    id_producto: int,
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    return actualizar_producto(db, id_producto, producto)


#RUTA PARA ELIMINAR UN PRODUCTO
@router.delete("/productos/{id_producto}")
def delete_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    return eliminar_producto(db, id_producto)