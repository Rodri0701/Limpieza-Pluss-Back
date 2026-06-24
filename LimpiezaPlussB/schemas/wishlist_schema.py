from pydantic import BaseModel
from datetime import datetime

# 1. ESQUEMA BASE (Lo único que le pedimos al usuario es qué producto quiere)
class WishlistBase(BaseModel):
    producto_id: int

# 2. ESQUEMA CREATE
class WishlistCreate(WishlistBase):
    pass

# 3. ESQUEMA RESPONSE (Lo que le devolvemos)
class WishlistResponse(WishlistBase):
    id_wishlist: int
    user_id: int # Aquí sí le mostramos de quién es, para confirmar
    fecha_agregado: datetime

    model_config = {"from_attributes": True}