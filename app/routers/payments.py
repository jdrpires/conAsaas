from fastapi import APIRouter, HTTPException, status
from app.schemas.payment import PaymentCreateRequest, PaymentResponse
from app.services.payment import PaymentService
from app.core.logging import logger

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreateRequest):
    """
    Cria uma nova cobrança no Asaas.
    
    - **customer_id**: ID do cliente no Asaas
    - **value**: Valor da cobrança
    - **billingType**: CREDIT_CARD, BOLETO ou PIX
    - **dueDate**: Data de vencimento
    - **installmentCount**: Número de parcelas (apenas cartão)
    - **creditCard**: Dados do cartão (obrigatório para CREDIT_CARD)
    - **creditCardHolderInfo**: Dados do titular (obrigatório para CREDIT_CARD)
    """
    try:
        service = PaymentService()
        return await service.create_payment(payment)
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar pagamento: {str(e)}"
        )


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str):
    """
    Busca um pagamento pelo ID do Asaas.
    """
    try:
        service = PaymentService()
        return await service.get_payment(payment_id)
    except Exception as e:
        logger.error(f"Error fetching payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pagamento não encontrado: {str(e)}"
        )
