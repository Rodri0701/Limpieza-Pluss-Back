from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# 1. ESQUEMA BASE: Los campos comunes
class ServicioBase(BaseModel):
    nombre_Servicio: str
    precio: float = Field(gt=0)
    Descripcion: str
    Categoria: str
    Status_servicio: Literal["A", "O", "I"] = "A"
    fecha_reserva: Optional[datetime] = None 
    duracion_estimada_horas: Optional[float] = None


# 2. HEREDA LO DE LA BASE
class ServicioCreate(ServicioBase):
    pass # Hereda todo tal cual de ServicioBase

class ServicioUpdate(BaseModel):
    nombre_Servicio: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    Descripcion: Optional[str] = None
    Categoria: Optional[str] = None
    Status_servicio: Optional[Literal["A", "O", "I"]] = None
    fecha_reserva: Optional[datetime] = None 
    duracion_estimada_horas: Optional[float] = None

# 4. ESQUEMA RESPONSE: El "Filtro" para la respuesta
class ServicioResponse(ServicioBase):
    id_Servicio: int
    #user_id: Optional[int] = None # Por si necesitas devolver qué usuario hizo la reserva

    model_config = {"from_attributes": True}