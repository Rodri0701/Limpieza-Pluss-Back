from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# 1. Schema Base: Atributos comunes que comparten todos los schemas
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    edad: int = Field(..., ge=0, le=120) # Debe ser mayor o igual a 0 y menor a 120
    calle: Optional[str] = None
    colonia: Optional[str] = None
    num_exterior: Optional[str] = Field(None, max_length=20)
    


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8) #  que tenga mínimo 8 caracteres

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    calle: Optional[str] = None
    colonia: Optional[str] = None
    num_exterior: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6)
   

class UsuarioResponse(UsuarioBase):
    id_user: int

    # Forma actualizada para Pydantic V2
    model_config = {"from_attributes": True}
    
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str