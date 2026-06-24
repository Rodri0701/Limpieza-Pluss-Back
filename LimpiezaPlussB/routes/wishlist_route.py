from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import SessionLocal
from ..schemas.wishlist_schema import WishlistCreate, WishlistResponse
from ..services.wishlist_service import agregar_a_wishlist, obtener_mi_wishlist, eliminar_de_wishlist

# Importamos a nuestro cadenero y modelo de usuarios
from ..config.dependencies import obtener_usuario_actual
from ..models.user_model import Usuarios

router = APIRouter(tags=["Wishlist"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. AGREGAR PRODUCTO A MI WISHLIST

@router.post("/wishlist/me", response_model=WishlistResponse)
def agregar_favorito(
    wishlist_in: WishlistCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    """Agrega un producto a la Wishlist del usuario autenticado."""
    # Le pasamos al servicio el ID sacado directamente del Token
    return agregar_a_wishlist(db=db, wishlist_in=wishlist_in, user_id=usuario_actual.id_user)


# 2. VER MI WISHLIST COMPLETA

@router.get("/wishlist/me", response_model=List[WishlistResponse])
def ver_favoritos(
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    """Devuelve todos los productos en la Wishlist del usuario autenticado."""
    return obtener_mi_wishlist(db=db, user_id=usuario_actual.id_user)


# 3. QUITAR UN PRODUCTO DE MI WISHLIST

@router.delete("/wishlist/me/{id_wishlist}")
def quitar_favorito(
    id_wishlist: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    """Elimina un registro específico de la Wishlist."""
    return eliminar_de_wishlist(db=db, id_wishlist=id_wishlist, user_id=usuario_actual.id_user)