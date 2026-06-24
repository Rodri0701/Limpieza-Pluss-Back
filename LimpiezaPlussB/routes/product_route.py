from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..schemas.product_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from ..services.product_service import (
    crear_producto, obtener_producto, obtener_productos, 
    actualizar_producto, eliminar_producto
)
from ..config.database import SessionLocal
from ..models.user_model import Usuarios
from ..config.dependencies import obtener_usuario_admin

# Agregamos el tag para agrupar todo bonito en Swagger
router = APIRouter(tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 1. CREAR (Solo Admin)
# ==========================================
@router.post("/productos/", response_model=ProductoResponse)
def crear(
    producto: ProductoCreate, 
    db: Session = Depends(get_db), 
    admin: Usuarios = Depends(obtener_usuario_admin)
):
    print(f"El admin {admin.nombre} está creando el producto: {producto.nombre_producto}")
    # Le pasamos el ID del admin al servicio
    return crear_producto(db=db, producto=producto, admin_id=admin.id_user)

# ==========================================
# 2. VER TODOS (Público)
# ==========================================
@router.get("/productos/", response_model=List[ProductoResponse])
def view_productos(db: Session = Depends(get_db)):
    return obtener_productos(db)

# ==========================================
# 3. VER POR ID (Público)
# ==========================================
@router.get("/productos/{id_producto}", response_model=ProductoResponse)
def view_producto(id_producto: int, db: Session = Depends(get_db)):
    return obtener_producto(db, id_producto)

# ==========================================
# 4. ACTUALIZAR (Solo Admin)
# ==========================================
@router.put("/productos/{id_producto}", response_model=ProductoResponse)
def actualizar(
    id_producto: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),
    admin: Usuarios = Depends(obtener_usuario_admin)
):
    return actualizar_producto(db=db, id_producto=id_producto, producto_actualizado=producto, admin_id=admin.id_user)

# ==========================================
# 5. ELIMINAR (Solo Admin)
# ==========================================
@router.delete("/productos/{id_producto}")
def delete_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    admin: Usuarios = Depends(obtener_usuario_admin)
):
    return eliminar_producto(db=db, id_producto=id_producto, admin_id=admin.id_user)