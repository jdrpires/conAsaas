# Roadmap de Melhorias - ConAssas API

## 🔒 Segurança

### Autenticação JWT
```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Validação de Webhook com Assinatura
```python
import hmac
import hashlib

def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
```

## 💾 Persistência de Dados

### Modelo de Banco de Dados (SQLAlchemy)
```python
# app/models/payment.py
from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    RECEIVED = "RECEIVED"
    OVERDUE = "OVERDUE"
    REFUNDED = "REFUNDED"

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    billing_type = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

## 🔄 Retry com Exponential Backoff

```python
# app/utils/retry.py
import asyncio
from functools import wraps

def async_retry(max_attempts=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

# Uso
@async_retry(max_attempts=3, base_delay=2)
async def create_payment_with_retry(payment_data):
    return await asaas_client.create_payment(payment_data)
```

## 📊 Cache com Redis

```python
# app/core/cache.py
import redis.asyncio as redis
import json
from typing import Optional

class CacheService:
    def __init__(self):
        self.redis = redis.from_url("redis://localhost:6379")
    
    async def get(self, key: str) -> Optional[dict]:
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: dict, expire: int = 300):
        await self.redis.set(key, json.dumps(value), ex=expire)
    
    async def delete(self, key: str):
        await self.redis.delete(key)

# Uso no serviço
async def get_customer(self, customer_id: str):
    cache_key = f"customer:{customer_id}"
    cached = await cache.get(cache_key)
    
    if cached:
        return CustomerResponse(**cached)
    
    result = await self.asaas_client.get_customer(customer_id)
    await cache.set(cache_key, result, expire=600)
    return CustomerResponse(**result)
```

## 🔔 Fila de Processamento (Celery)

```python
# app/tasks/celery_app.py
from celery import Celery

celery_app = Celery(
    "conassas",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(bind=True, max_retries=3)
def process_webhook(self, event_data):
    try:
        # Processar webhook de forma assíncrona
        payment_id = event_data["payment"]["id"]
        event_type = event_data["event"]
        
        # Atualizar banco de dados
        # Enviar notificações
        # Disparar eventos
        
        return {"status": "processed", "payment_id": payment_id}
    except Exception as e:
        self.retry(exc=e, countdown=60)
```

## 💰 Split de Pagamentos

```python
# app/schemas/split.py
from pydantic import BaseModel
from typing import List

class SplitReceiver(BaseModel):
    walletId: str
    percentualValue: float  # Percentual do valor total
    
class PaymentWithSplit(PaymentCreateRequest):
    split: List[SplitReceiver]

# No serviço
async def create_payment_with_split(self, payment_data: PaymentWithSplit):
    payload = {
        **payment_data.model_dump(exclude={"split"}),
        "split": [s.model_dump() for s in payment_data.split]
    }
    return await self.asaas_client.create_payment(payload)
```

## 🔁 Assinaturas Recorrentes

```python
# app/schemas/subscription.py
from pydantic import BaseModel
from typing import Literal

class SubscriptionCreate(BaseModel):
    customer_id: str
    billingType: Literal["CREDIT_CARD", "BOLETO"]
    value: float
    cycle: Literal["WEEKLY", "BIWEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]
    description: str

# app/services/subscription.py
class SubscriptionService:
    async def create_subscription(self, data: SubscriptionCreate):
        payload = {
            "customer": data.customer_id,
            "billingType": data.billingType,
            "value": data.value,
            "cycle": data.cycle,
            "description": data.description
        }
        return await self.asaas_client._request("POST", "subscriptions", payload)
```

## 📈 Métricas e Observabilidade

```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram
import time

request_count = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

## 🏢 Multi-tenancy

```python
# app/models/tenant.py
class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    asaas_api_key = Column(String, nullable=False)
    asaas_wallet_id = Column(String)
    is_active = Column(Boolean, default=True)

# Middleware para identificar tenant
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        return JSONResponse(
            status_code=400,
            content={"detail": "X-Tenant-ID header required"}
        )
    
    # Buscar configurações do tenant
    tenant = await get_tenant(tenant_id)
    request.state.tenant = tenant
    
    return await call_next(request)
```

## 🔍 Rate Limiting

```python
# app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/payments")
@limiter.limit("10/minute")
async def create_payment(request: Request, payment: PaymentCreateRequest):
    # ...
```

## 📊 Dashboard Administrativo

Sugestões de tecnologias:
- **Frontend:** React + TypeScript + Tailwind CSS
- **Gráficos:** Recharts ou Chart.js
- **Tabelas:** TanStack Table (React Table)

Funcionalidades:
- Visualização de pagamentos em tempo real
- Filtros por status, data, cliente
- Exportação de relatórios (CSV, PDF)
- Gráficos de receita
- Gestão de clientes
- Configuração de webhooks

## 🧪 Testes Completos

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_asaas_client(mocker):
    return mocker.patch("app.clients.asaas.AsaasClient")

# tests/test_payments.py
@pytest.mark.asyncio
async def test_create_pix_payment(client, mock_asaas_client):
    mock_asaas_client.return_value.create_payment.return_value = {
        "id": "pay_123",
        "status": "PENDING",
        "value": 100.00,
        "billingType": "PIX",
        "dueDate": "2026-02-15"
    }
    
    response = await client.post("/payments", json={
        "customer_id": "cus_123",
        "value": 100.00,
        "billingType": "PIX",
        "dueDate": "2026-02-15"
    })
    
    assert response.status_code == 201
    assert response.json()["billingType"] == "PIX"
```

## 🚀 Deploy em Produção

### AWS ECS com Fargate
```yaml
# ecs-task-definition.json
{
  "family": "conassas-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [{
    "name": "api",
    "image": "your-ecr-repo/conassas-api:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "ENVIRONMENT", "value": "production"}
    ],
    "secrets": [
      {"name": "ASAAS_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
    ]
  }]
}
```

### Kubernetes
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: conassas-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: conassas-api
  template:
    metadata:
      labels:
        app: conassas-api
    spec:
      containers:
      - name: api
        image: conassas-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ASAAS_API_KEY
          valueFrom:
            secretKeyRef:
              name: asaas-credentials
              key: api-key
```

## 📝 Logging Estruturado Avançado

```python
# app/core/logging.py
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Uso
logger.info("payment_created", 
    payment_id="pay_123",
    customer_id="cus_456",
    value=100.00,
    billing_type="PIX"
)
```
