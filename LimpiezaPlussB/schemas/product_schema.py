from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. ESQUEMA BASE (Lo que comparten la creación y la respuesta)
class ProductoBase(BaseModel):
    nombre_producto: str
    precio: float = Field(gt=0)
    descripcion: str
    categoria: str
    stock: int = Field(ge=0) # Cambié a 0, ¡podrías quedarte sin stock válido!
    descuento: int = Field(default=0, ge=0, le=100) # Porcentaje de 0 a 100

# 2. ESQUEMA DE CREACIÓN (Lo que pide el JSON al usuario)
class ProductoCreate(ProductoBase):
    pass # Hereda todo tal cual de ProductoBase

# 3. ESQUEMA DE ACTUALIZACIÓN (Todo es opcional)
class ProductoUpdate(BaseModel):
    nombre_producto: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    stock: Optional[int] = Field(default=None, ge=0)
    descuento: Optional[int] = Field(default=None, ge=0, le=100)

# 4. ESQUEMA DE RESPUESTA (Lo que le devolvemos al frontend/Swagger)
class ProductoResponse(ProductoBase):
    id_producto: int
    status: str
    fecha_creacion: datetime
    # Hacemos opcionales los campos de auditoría porque al inicio estarán vacíos
    user_alta: Optional[int] = None 
    user_update: Optional[int] = None
    fecha_update: Optional[datetime] = None
    
    model_config = {"from_attributes": True} 