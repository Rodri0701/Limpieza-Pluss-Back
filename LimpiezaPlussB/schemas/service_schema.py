from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. ESQUEMA BASE: Los campos comunes (Catálogo Puro)
class ServicioBase(BaseModel):
    nombre_servicio: str
    precio: float = Field(gt=0)
    descripcion: str
    categoria: str
    duracion_estimada_horas: Optional[float] = Field(default=None, gt=0)

# 2. HEREDA LO DE LA BASE
class ServicioCreate(ServicioBase):
    pass # Hereda todo tal cual de ServicioBase

# 3. ESQUEMA DE ACTUALIZACIÓN (Todo opcional para ediciones parciales)
class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    duracion_estimada_horas: Optional[float] = None

# 4. ESQUEMA RESPONSE: El "Filtro" para la respuesta hacia el Frontend
class ServicioResponse(ServicioBase):
    id_servicio: int
    status: str
    fecha_creacion: datetime
    # Mostramos quién ha interactuado con este servicio de forma opcional
    user_alta: Optional[int] = None 
    user_update: Optional[int] = None
    fecha_update: Optional[datetime] = None

    model_config = {"from_attributes": True}