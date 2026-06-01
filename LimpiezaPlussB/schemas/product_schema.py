from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre_Producto:str
    precio: float
    Descripcion : str
    Categoria :str
    Stock : int