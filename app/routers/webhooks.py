from fastapi import APIRouter, HTTPException, status, Request
from app.schemas.webhook import WebhookEvent, WebhookResponse
from app.core.logging import logger
from datetime import datetime

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Armazena eventos processados para idempotência (em produção, usar Redis/DB)
processed_events = set()


@router.post("/asaas", response_model=WebhookResponse)
async def asaas_webhook(event: WebhookEvent, request: Request):
    """
    Recebe webhooks do Asaas para atualização de status de pagamentos.
    
    Eventos suportados:
    - PAYMENT_CREATED: Pagamento criado
    - PAYMENT_CONFIRMED: Pagamento confirmado
    - PAYMENT_RECEIVED: Pagamento recebido
    - PAYMENT_OVERDUE: Pagamento vencido
    - PAYMENT_DELETED: Pagamento deletado
    - PAYMENT_REFUNDED: Pagamento estornado
    """
    payment_id = event.payment.get("id")
    event_key = f"{event.event}:{payment_id}"
    
    # Idempotência: verifica se evento já foi processado
    if event_key in processed_events:
        logger.info(f"Event already processed: {event_key}")
        return WebhookResponse(
            received=True,
            payment_id=payment_id,
            event=event.event,
            processed_at=datetime.now()
        )
    
    logger.info(f"Processing webhook: {event.event} for payment {payment_id}")
    
    try:
        # Aqui você implementaria a lógica de atualização no seu banco de dados
        # Exemplo:
        # - Atualizar status do pagamento
        # - Enviar notificação ao cliente
        # - Disparar eventos internos
        # - Atualizar estoque/serviço
        
        if event.event == "PAYMENT_CONFIRMED":
            logger.info(f"Payment {payment_id} confirmed - Value: {event.payment.get('value')}")
            # await update_payment_status(payment_id, "CONFIRMED")
            # await notify_customer(payment_id)
        
        elif event.event == "PAYMENT_RECEIVED":
            logger.info(f"Payment {payment_id} received")
            # await update_payment_status(payment_id, "RECEIVED")
            # await release_product(payment_id)
        
        elif event.event == "PAYMENT_OVERDUE":
            logger.warning(f"Payment {payment_id} is overdue")
            # await update_payment_status(payment_id, "OVERDUE")
            # await send_overdue_notification(payment_id)
        
        elif event.event == "PAYMENT_REFUNDED":
            logger.info(f"Payment {payment_id} refunded")
            # await update_payment_status(payment_id, "REFUNDED")
            # await process_refund(payment_id)
        
        # Marca evento como processado
        processed_events.add(event_key)
        
        return WebhookResponse(
            received=True,
            payment_id=payment_id,
            event=event.event,
            processed_at=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar webhook: {str(e)}"
        )
