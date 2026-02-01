# ConAssas API

API REST em Python com FastAPI para integração com o gateway de pagamento Asaas.

## Funcionalidades

- ✅ Criar clientes (Pessoa Física e Jurídica)
- ✅ Gerar cobranças via Cartão de Crédito (com parcelamento)
- ✅ Gerar cobranças via Boleto Bancário
- ✅ Gerar cobranças via PIX (com QR Code)
- ✅ Receber webhooks do Asaas
- ✅ Validação de dados com Pydantic
- ✅ Logging estruturado
- ✅ Tratamento de erros
- ✅ Arquitetura limpa e modular

## Tecnologias

- Python 3.11+
- FastAPI
- Pydantic v2
- httpx (async)
- uvicorn

## Estrutura do Projeto

```
conAssas/
├── app/
│   ├── main.py              # Aplicação FastAPI
│   ├── core/
│   │   ├── config.py        # Configurações e variáveis de ambiente
│   │   └── logging.py       # Setup de logging
│   ├── schemas/
│   │   ├── customer.py      # Schemas de cliente
│   │   ├── payment.py       # Schemas de pagamento
│   │   └── webhook.py       # Schemas de webhook
│   ├── clients/
│   │   └── asaas.py         # Cliente HTTP para Asaas
│   ├── services/
│   │   ├── customer.py      # Lógica de negócio de clientes
│   │   └── payment.py       # Lógica de negócio de pagamentos
│   └── routers/
│       ├── customers.py     # Endpoints de clientes
│       ├── payments.py      # Endpoints de pagamentos
│       └── webhooks.py      # Endpoints de webhooks
├── .env                     # Variáveis de ambiente (não commitar)
├── .env.example             # Exemplo de variáveis
├── requirements.txt         # Dependências
└── README.md
```

## Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd conAssas
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
ASAAS_API_KEY=sua_chave_api_aqui
ASAAS_BASE_URL=https://sandbox.asaas.com/api/v3
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Importante:** Para produção, altere a URL para `https://api.asaas.com/v3`

## Executar a API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Endpoints

### 1. Criar Cliente

**POST** `/customers`

```json
{
  "name": "João Silva",
  "cpfCnpj": "12345678901",
  "email": "joao@example.com",
  "phone": "11999999999",
  "address": {
    "address": "Rua Exemplo",
    "addressNumber": "123",
    "complement": "Apto 45",
    "province": "Centro",
    "postalCode": "01310-100"
  }
}
```

**Resposta:**
```json
{
  "id": "cus_000005161077",
  "name": "João Silva",
  "cpfCnpj": "12345678901",
  "email": "joao@example.com",
  "phone": "11999999999"
}
```

### 2. Criar Pagamento - PIX

**POST** `/payments`

```json
{
  "customer_id": "cus_000005161077",
  "value": 100.50,
  "billingType": "PIX",
  "dueDate": "2026-02-15",
  "description": "Pagamento de teste"
}
```

**Resposta:**
```json
{
  "id": "pay_123456789",
  "status": "PENDING",
  "value": 100.50,
  "billingType": "PIX",
  "dueDate": "2026-02-15",
  "invoiceUrl": "https://...",
  "pixQrCodeUrl": "data:image/png;base64,...",
  "pixCopyPaste": "00020126580014br.gov.bcb.pix..."
}
```

### 3. Criar Pagamento - Boleto

**POST** `/payments`

```json
{
  "customer_id": "cus_000005161077",
  "value": 250.00,
  "billingType": "BOLETO",
  "dueDate": "2026-02-20",
  "description": "Mensalidade"
}
```

**Resposta:**
```json
{
  "id": "pay_987654321",
  "status": "PENDING",
  "value": 250.00,
  "billingType": "BOLETO",
  "dueDate": "2026-02-20",
  "invoiceUrl": "https://...",
  "bankSlipUrl": "https://..."
}
```

### 4. Criar Pagamento - Cartão de Crédito

**POST** `/payments`

```json
{
  "customer_id": "cus_000005161077",
  "value": 500.00,
  "billingType": "CREDIT_CARD",
  "dueDate": "2026-02-10",
  "installmentCount": 3,
  "creditCard": {
    "holderName": "João Silva",
    "number": "5162306219378829",
    "expiryMonth": "12",
    "expiryYear": "2028",
    "ccv": "123"
  },
  "creditCardHolderInfo": {
    "name": "João Silva",
    "email": "joao@example.com",
    "cpfCnpj": "12345678901",
    "postalCode": "01310-100",
    "addressNumber": "123",
    "phone": "11999999999"
  }
}
```

**Resposta:**
```json
{
  "id": "pay_555666777",
  "status": "CONFIRMED",
  "value": 500.00,
  "billingType": "CREDIT_CARD",
  "dueDate": "2026-02-10",
  "invoiceUrl": "https://..."
}
```

### 5. Buscar Pagamento

**GET** `/payments/{payment_id}`

### 6. Buscar Cliente

**GET** `/customers/{customer_id}`

### 7. Webhook Asaas

**POST** `/webhooks/asaas`

Recebe notificações automáticas do Asaas sobre mudanças de status.

```json
{
  "event": "PAYMENT_CONFIRMED",
  "payment": {
    "id": "pay_123456789",
    "value": 100.50,
    "status": "CONFIRMED",
    "billingType": "PIX"
  }
}
```

## Configurar Webhooks no Asaas

1. Acesse o painel do Asaas
2. Vá em **Configurações > Webhooks**
3. Adicione a URL: `https://seu-dominio.com/webhooks/asaas`
4. Selecione os eventos desejados

## Segurança

- ✅ Não armazena dados sensíveis de cartão
- ✅ Validação de CPF/CNPJ
- ✅ Validação de payloads com Pydantic
- ✅ Idempotência no webhook
- ✅ Logs estruturados
- ⚠️ Implementar autenticação JWT para endpoints (próxima versão)
- ⚠️ Validar origem dos webhooks com token/assinatura

## Melhorias Futuras

### Curto Prazo
- [ ] Autenticação JWT
- [ ] Validação de assinatura de webhooks
- [ ] Persistência em banco de dados (PostgreSQL)
- [ ] Cache com Redis
- [ ] Testes unitários e de integração

### Médio Prazo
- [ ] Suporte a assinaturas recorrentes
- [ ] Split de pagamentos
- [ ] Retry automático com exponential backoff
- [ ] Fila de processamento (Celery/RabbitMQ)
- [ ] Métricas e observabilidade (Prometheus/Grafana)

### Longo Prazo
- [ ] Multi-tenancy
- [ ] Suporte a múltiplos gateways
- [ ] Dashboard administrativo
- [ ] Relatórios e analytics

## Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest
```

## Produção

### Usando Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t conassas-api .
docker run -p 8000:8000 --env-file .env conassas-api
```

### Usando Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Documentação Asaas

- [Documentação Oficial](https://docs.asaas.com)
- [API Reference](https://docs.asaas.com/reference)
- [Sandbox](https://sandbox.asaas.com)

## Licença

MIT

## Autor

Desenvolvido para integração com Asaas
