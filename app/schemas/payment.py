from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import date
from decimal import Decimal


class CreditCardHolderInfo(BaseModel):
    name: str
    email: str
    cpfCnpj: str
    postalCode: str
    addressNumber: str
    phone: str


class CreditCard(BaseModel):
    holderName: str
    number: str
    expiryMonth: str
    expiryYear: str
    ccv: str


class PaymentCreateRequest(BaseModel):
    customer_id: str
    value: Decimal = Field(..., gt=0, decimal_places=2)
    billingType: Literal["CREDIT_CARD", "BOLETO", "PIX"]
    dueDate: date
    description: Optional[str] = None
    installmentCount: Optional[int] = Field(default=1, ge=1, le=12)
    creditCard: Optional[CreditCard] = None
    creditCardHolderInfo: Optional[CreditCardHolderInfo] = None
    
    @field_validator('creditCard')
    @classmethod
    def validate_credit_card(cls, v, info):
        if info.data.get('billingType') == 'CREDIT_CARD' and not v:
            raise ValueError('creditCard é obrigatório para pagamento com cartão')
        return v
    
    @field_validator('creditCardHolderInfo')
    @classmethod
    def validate_holder_info(cls, v, info):
        if info.data.get('billingType') == 'CREDIT_CARD' and not v:
            raise ValueError('creditCardHolderInfo é obrigatório para pagamento com cartão')
        return v


class PaymentResponse(BaseModel):
    id: str
    status: str
    value: Decimal
    billingType: str
    dueDate: date
    invoiceUrl: Optional[str] = None
    bankSlipUrl: Optional[str] = None
    pixQrCodeUrl: Optional[str] = None
    pixCopyPaste: Optional[str] = None
