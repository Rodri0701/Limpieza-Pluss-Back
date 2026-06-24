from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
import re

from ..models.product_model import Producto
from ..schemas.product_schema import ProductoCreate, ProductoUpdate

# ==========================================
# 1. CREAR PRODUCTO
# ==========================================
def crear_producto(db: Session, producto: ProductoCreate, admin_id: int):
    # 1. Limpieza de datos
    producto.nombre_producto = producto.nombre_producto.strip() 
    
    # 2. Validaciones estrictas
    if not producto.nombre_producto:
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")
        
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]+$', producto.nombre_producto):
        raise HTTPException(status_code=400, detail="Nombre con caracteres inválidos")

    if producto.precio >= 100000:
        raise HTTPException(status_code=400, detail="Precio extremadamente fuera de rango")

    if producto.stock >= 10000:
        raise HTTPException(status_code=400, detail="No puedes agregar tanto a existencia")

    # 3. Verificar duplicados (usamos lower para evitar que "JABÓN" y "jabón" existan a la vez)
    existe = db.query(Producto).filter(
        func.lower(Producto.nombre_producto) == producto.nombre_producto.lower()
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="Este producto ya existe en el catálogo.")

    # 4. Crear el producto asignando el ID del administrador real
    nuevo_producto = Producto(
        **producto.model_dump(),
        user_alta=admin_id  # Guardamos quién lo creó
    ) 
    
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    
    return nuevo_producto

# ==========================================
# 2. LEER PRODUCTO POR ID
# ==========================================
def obtener_producto(db: Session, id_producto: int):
    # Solo mostramos productos que sigan activos ("A")
    producto = db.query(Producto).filter(
        Producto.id_producto == id_producto,
        Producto.status == "A"
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o descontinuado")

    return producto

# ==========================================
# 3. LEER TODOS LOS PRODUCTOS
# ==========================================
def obtener_productos(db: Session):
    # Solo traemos los activos
    return db.query(Producto).filter(Producto.status == "A").all()

# ==========================================
# 4. ACTUALIZAR PRODUCTO
# ==========================================
def actualizar_producto(db: Session, id_producto: int, producto_actualizado: ProductoUpdate, admin_id: int):
    producto = db.query(Producto).filter(
        Producto.id_producto == id_producto,
        Producto.status == "A"
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Extraemos solo los campos que el usuario realmente envió (exclude_unset=True)
    datos = producto_actualizado.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(producto, campo, valor)
        
    # Auditoría: Quién lo editó (La fecha se actualiza sola por el onupdate del modelo)
    producto.user_update = admin_id

    db.commit()
    db.refresh(producto)

    return producto

# ==========================================
# 5. ELIMINAR PRODUCTO (SOFT DELETE)
# ==========================================
def eliminar_producto(db: Session, id_producto: int, admin_id: int):
    producto = db.query(Producto).filter(
        Producto.id_producto == id_producto,
        Producto.status == "A"
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Aplicamos el Borrado Lógico
    producto.status = "I"
    producto.user_update = admin_id # Registramos quién lo eliminó

    db.commit()
    
    return {"mensaje": f"Producto '{producto.nombre_producto}' eliminado exitosamente."}