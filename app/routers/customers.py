from fastapi import APIRouter, HTTPException, status
from app.schemas.customer import CustomerCreateRequest, CustomerResponse
from app.services.customer import CustomerService
from app.core.logging import logger

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreateRequest):
    """
    Cria um novo cliente no Asaas.
    
    - **name**: Nome completo do cliente
    - **cpfCnpj**: CPF (11 dígitos) ou CNPJ (14 dígitos)
    - **email**: Email válido
    - **phone**: Telefone com DDD
    - **address**: Endereço completo (opcional)
    """
    try:
        service = CustomerService()
        return await service.create_customer(customer)
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str):
    """
    Busca um cliente pelo ID do Asaas.
    """
    try:
        service = CustomerService()
        return await service.get_customer(customer_id)
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente não encontrado: {str(e)}"
        )
