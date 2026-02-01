import httpx
from typing import Any, Optional
from app.core.config import get_settings
from app.core.logging import logger


class AsaasClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.asaas_base_url
        self.headers = {
            "Content-Type": "application/json",
            "access_token": self.settings.asaas_api_key
        }
        logger.info(f"AsaasClient initialized with key: {self.settings.asaas_api_key[:30]}...")
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[dict] = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    timeout=30.0
                )
                
                logger.info(f"Asaas API {method} {endpoint} - Status: {response.status_code}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Asaas API error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                raise
    
    async def create_customer(self, customer_data: dict) -> dict:
        return await self._request("POST", "customers", customer_data)
    
    async def get_customer(self, customer_id: str) -> dict:
        return await self._request("GET", f"customers/{customer_id}")
    
    async def create_payment(self, payment_data: dict) -> dict:
        return await self._request("POST", "payments", payment_data)
    
    async def get_payment(self, payment_id: str) -> dict:
        return await self._request("GET", f"payments/{payment_id}")
    
    async def get_pix_qrcode(self, payment_id: str) -> dict:
        return await self._request("GET", f"payments/{payment_id}/pixQrCode")
