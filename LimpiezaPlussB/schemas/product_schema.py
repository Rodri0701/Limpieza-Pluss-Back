from pydantic import BaseModel, Field, StrictInt
from datetime import datetime

class ProductoCreate(BaseModel):
    nombre_Producto:str
    precio: float = Field(gt=0)
    Descripcion : str
    Categoria :str
    Stock : int = Field(ge=5)
    descuento : StrictInt
    fecha_creacion : datetime
   # user_alta : str