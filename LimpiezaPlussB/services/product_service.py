from sqlalchemy.orm import Session
from ..models.product_model import Producto

def crear_producto(db: Session, producto):
    nuevo_producto = Producto(
    nombre_Producto=producto.nombre_Producto,
    precio=producto.precio,
    Descripcion=producto.Descripcion,
    Categoria=producto.Categoria,
    Stock=producto.Stock
    )
        
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    
    return nuevo_producto