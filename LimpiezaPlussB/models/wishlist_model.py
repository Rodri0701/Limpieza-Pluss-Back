from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..config.database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    # ID principal de la tabla
    id_wishlist = Column(Integer, primary_key=True, index=True)

    # Llave Foránea 1:(Conecta con la tabla de usuarios)
    user_id = Column(Integer, ForeignKey("usuarios.id_user"), nullable=False)

    # Llave Foránea 2: (Conecta con la tabla de productos)
    
    producto_id = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)

    # Auditoría: ¿Cuándo lo agregó?
    fecha_agregado = Column(DateTime, default=func.now())