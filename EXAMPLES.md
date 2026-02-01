# Exemplos de Payloads - ConAssas API

## 1. Criar Cliente - Pessoa Física

```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "cpfCnpj": "12345678901",
    "email": "joao.silva@example.com",
    "phone": "11999999999",
    "address": {
      "address": "Rua das Flores",
      "addressNumber": "123",
      "complement": "Apto 45",
      "province": "Centro",
      "postalCode": "01310-100"
    }
  }'
```

## 2. Criar Cliente - Pessoa Jurídica

```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Empresa LTDA",
    "cpfCnpj": "12345678000190",
    "email": "contato@empresa.com.br",
    "phone": "1133334444"
  }'
```

## 3. Criar Pagamento - PIX

```bash
curl -X POST "http://localhost:8000/payments" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_000005161077",
    "value": 150.00,
    "billingType": "PIX",
    "dueDate": "2026-02-15",
    "description": "Pagamento via PIX"
  }'
```

## 4. Criar Pagamento - Boleto

```bash
curl -X POST "http://localhost:8000/payments" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_000005161077",
    "value": 250.00,
    "billingType": "BOLETO",
    "dueDate": "2026-02-20",
    "description": "Mensalidade - Janeiro/2026"
  }'
```

## 5. Criar Pagamento - Cartão de Crédito (À vista)

```bash
curl -X POST "http://localhost:8000/payments" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_000005161077",
    "value": 500.00,
    "billingType": "CREDIT_CARD",
    "dueDate": "2026-02-10",
    "installmentCount": 1,
    "description": "Compra à vista",
    "creditCard": {
      "holderName": "João Silva",
      "number": "5162306219378829",
      "expiryMonth": "12",
      "expiryYear": "2028",
      "ccv": "123"
    },
    "creditCardHolderInfo": {
      "name": "João Silva",
      "email": "joao.silva@example.com",
      "cpfCnpj": "12345678901",
      "postalCode": "01310-100",
      "addressNumber": "123",
      "phone": "11999999999"
    }
  }'
```

## 6. Criar Pagamento - Cartão de Crédito (Parcelado)

```bash
curl -X POST "http://localhost:8000/payments" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_000005161077",
    "value": 1200.00,
    "billingType": "CREDIT_CARD",
    "dueDate": "2026-02-10",
    "installmentCount": 6,
    "description": "Compra parcelada em 6x",
    "creditCard": {
      "holderName": "João Silva",
      "number": "5162306219378829",
      "expiryMonth": "12",
      "expiryYear": "2028",
      "ccv": "123"
    },
    "creditCardHolderInfo": {
      "name": "João Silva",
      "email": "joao.silva@example.com",
      "cpfCnpj": "12345678901",
      "postalCode": "01310-100",
      "addressNumber": "123",
      "phone": "11999999999"
    }
  }'
```

## 7. Buscar Cliente

```bash
curl -X GET "http://localhost:8000/customers/cus_000005161077"
```

## 8. Buscar Pagamento

```bash
curl -X GET "http://localhost:8000/payments/pay_123456789"
```

## 9. Webhook - Pagamento Confirmado

```bash
curl -X POST "http://localhost:8000/webhooks/asaas" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "PAYMENT_CONFIRMED",
    "payment": {
      "id": "pay_123456789",
      "value": 150.00,
      "status": "CONFIRMED",
      "billingType": "PIX",
      "customer": "cus_000005161077"
    }
  }'
```

## 10. Webhook - Pagamento Vencido

```bash
curl -X POST "http://localhost:8000/webhooks/asaas" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "PAYMENT_OVERDUE",
    "payment": {
      "id": "pay_987654321",
      "value": 250.00,
      "status": "OVERDUE",
      "billingType": "BOLETO",
      "customer": "cus_000005161077"
    }
  }'
```

## Cartões de Teste (Sandbox Asaas)

### Aprovado
- **Número:** 5162306219378829
- **Validade:** 12/2028
- **CVV:** 123
- **Nome:** Qualquer nome

### Recusado
- **Número:** 5162306219378837
- **Validade:** 12/2028
- **CVV:** 123

### Análise
- **Número:** 5162306219378845
- **Validade:** 12/2028
- **CVV:** 123

## Testando com Python

```python
import httpx
import asyncio

async def test_create_customer():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/customers",
            json={
                "name": "Maria Santos",
                "cpfCnpj": "98765432100",
                "email": "maria@example.com",
                "phone": "11988887777"
            }
        )
        print(response.json())

asyncio.run(test_create_customer())
```

## Testando com JavaScript/Node.js

```javascript
const axios = require('axios');

async function createPayment() {
  const response = await axios.post('http://localhost:8000/payments', {
    customer_id: 'cus_000005161077',
    value: 100.00,
    billingType: 'PIX',
    dueDate: '2026-02-15',
    description: 'Teste PIX'
  });
  
  console.log(response.data);
}

createPayment();
```
