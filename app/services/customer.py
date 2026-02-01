from app.clients.asaas import AsaasClient
from app.schemas.customer import CustomerCreateRequest, CustomerResponse
from app.core.logging import logger


class CustomerService:
    def __init__(self):
        self.asaas_client = AsaasClient()
    
    async def create_customer(self, customer_data: CustomerCreateRequest) -> CustomerResponse:
        logger.info(f"Creating customer: {customer_data.email}")
        
        payload = customer_data.model_dump(exclude_none=True)
        
        result = await self.asaas_client.create_customer(payload)
        
        return CustomerResponse(
            id=result["id"],
            name=result["name"],
            cpfCnpj=result["cpfCnpj"],
            email=result["email"],
            phone=result["phone"]
        )
    
    async def get_customer(self, customer_id: str) -> CustomerResponse:
        logger.info(f"Fetching customer: {customer_id}")
        
        result = await self.asaas_client.get_customer(customer_id)
        
        return CustomerResponse(
            id=result["id"],
            name=result["name"],
            cpfCnpj=result["cpfCnpj"],
            email=result["email"],
            phone=result["phone"]
        )
