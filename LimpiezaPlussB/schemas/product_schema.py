from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre_Producto:str
    precio: float = Field(gt=0)
    descripcion : str
    categoria :str
    stock : int = Field(ge=5)