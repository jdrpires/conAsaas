from app.clients.asaas import AsaasClient
from app.schemas.payment import PaymentCreateRequest, PaymentResponse
from app.core.logging import logger
from datetime import date


class PaymentService:
    def __init__(self):
        self.asaas_client = AsaasClient()
    
    async def create_payment(self, payment_data: PaymentCreateRequest) -> PaymentResponse:
        logger.info(f"Creating payment: {payment_data.billingType} - R$ {payment_data.value}")
        
        payload = {
            "customer": payment_data.customer_id,
            "billingType": payment_data.billingType,
            "value": float(payment_data.value),
            "dueDate": payment_data.dueDate.isoformat(),
        }
        
        if payment_data.description:
            payload["description"] = payment_data.description
        
        if payment_data.billingType == "CREDIT_CARD":
            payload["installmentCount"] = payment_data.installmentCount
            payload["installmentValue"] = float(payment_data.value) / payment_data.installmentCount
            payload["creditCard"] = payment_data.creditCard.model_dump()
            payload["creditCardHolderInfo"] = payment_data.creditCardHolderInfo.model_dump()
        
        result = await self.asaas_client.create_payment(payload)
        
        response = PaymentResponse(
            id=result["id"],
            status=result["status"],
            value=result["value"],
            billingType=result["billingType"],
            dueDate=date.fromisoformat(result["dueDate"]),
            invoiceUrl=result.get("invoiceUrl"),
            bankSlipUrl=result.get("bankSlipUrl")
        )
        
        if payment_data.billingType == "PIX":
            try:
                pix_data = await self.asaas_client.get_pix_qrcode(result["id"])
                response.pixQrCodeUrl = pix_data.get("encodedImage")
                response.pixCopyPaste = pix_data.get("payload")
            except Exception as e:
                logger.warning(f"Failed to get PIX QR Code: {str(e)}")
        
        return response
    
    async def get_payment(self, payment_id: str) -> PaymentResponse:
        logger.info(f"Fetching payment: {payment_id}")
        
        result = await self.asaas_client.get_payment(payment_id)
        
        return PaymentResponse(
            id=result["id"],
            status=result["status"],
            value=result["value"],
            billingType=result["billingType"],
            dueDate=date.fromisoformat(result["dueDate"]),
            invoiceUrl=result.get("invoiceUrl"),
            bankSlipUrl=result.get("bankSlipUrl")
        )
