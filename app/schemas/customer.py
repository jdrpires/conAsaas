from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class AddressSchema(BaseModel):
    address: str
    addressNumber: str
    complement: Optional[str] = None
    province: str
    postalCode: str


class CustomerCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    cpfCnpj: str = Field(..., min_length=11, max_length=18)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: Optional[AddressSchema] = None
    
    @field_validator('cpfCnpj')
    @classmethod
    def validate_cpf_cnpj(cls, v: str) -> str:
        cleaned = re.sub(r'\D', '', v)
        if len(cleaned) not in [11, 14]:
            raise ValueError('CPF deve ter 11 dígitos ou CNPJ 14 dígitos')
        return cleaned
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r'\D', '', v)
        if len(cleaned) < 10:
            raise ValueError('Telefone inválido')
        return cleaned


class CustomerResponse(BaseModel):
    id: str
    name: str
    cpfCnpj: str
    email: str
    phone: str
