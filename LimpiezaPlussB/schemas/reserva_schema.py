from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    servicio_id: int
    fecha_reserva: datetime 

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id_reserva: int
    user_id: int
    status: str
    
    model_config = {"from_attributes": True}