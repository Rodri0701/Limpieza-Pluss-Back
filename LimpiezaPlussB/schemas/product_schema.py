from pydantic import BaseModel, Field, StrictInt
from typing import Optional
from datetime import datetime

class ProductoCreate(BaseModel):
    nombre_Producto:str
    precio: float = Field(gt=0)
    Descripcion : str
    Categoria :str
    Stock : int = Field(ge=5)
    descuento : StrictInt
    #fecha_creacion : datetime
   # user_alta : str
   # user_update : str
    #fecha_update : datetime
   
class ProductoUpdate(BaseModel):
 nombre_Producto: Optional[str] = None
 precio: Optional[float] = Field(default=None, gt=0)
 Descripcion: Optional[str] = None
 Categoria: Optional[str] = None
 Stock: Optional[int] = Field(default=None, ge=5)
 descuento: Optional[float] = None
 #user_update : str
 #fecha_update : datetime