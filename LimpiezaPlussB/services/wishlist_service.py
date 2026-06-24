from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.wishlist_model import Wishlist
# Importa tu modelo de productos para validar que exista (ajusta la ruta)
from ..models.product_model import Producto 
from ..schemas.wishlist_schema import WishlistCreate

# 1. ADD MI WISHLIST

def agregar_a_wishlist(db: Session, wishlist_in: WishlistCreate, user_id: int):
    # BLINDAJE 1: Verificamos que el producto realmente exista en el catálogo
    producto_existe = db.query(Producto).filter(Producto.id_producto == wishlist_in.producto_id).first()
    if not producto_existe:
        raise HTTPException(status_code=404, detail="El producto no existe.")

    # Se revisa que no lo tenga repetido en su lista
    item_duplicado = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.producto_id == wishlist_in.producto_id
    ).first()
    
    if item_duplicado:
        raise HTTPException(status_code=400, detail="Este producto ya está en tu Wishlist.")

    # Si pasa las pruebas, lo guardamos uniendo el producto con el usuario del token
    nuevo_favorito = Wishlist(
        user_id=user_id,
        producto_id=wishlist_in.producto_id
    )
    db.add(nuevo_favorito)
    db.commit()
    db.refresh(nuevo_favorito)
    
    return nuevo_favorito


# 2. VER MI WISHLIST

def obtener_mi_wishlist(db: Session, user_id: int):
    # Solo traemos los registros que le pertenecen al usuario en sesión
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()


# 3. ELIMINAR DE MI WISHLIST

def eliminar_de_wishlist(db: Session, id_wishlist: int, user_id: int):
    # Buscamos el registro, PERO exigiendo que el user_id coincida (seguridad)
    item = db.query(Wishlist).filter(
        Wishlist.id_wishlist == id_wishlist, 
        Wishlist.user_id == user_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="El artículo no se encuentra en tu Wishlist o no te pertenece.")
        
    db.delete(item) 
    db.commit()
    
    return {"mensaje": "Producto eliminado de tus favoritos."}