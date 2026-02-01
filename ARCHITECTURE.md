# Arquitetura do Projeto ConAssas

## Visão Geral

A API ConAssas segue os princípios de **Clean Architecture** e **SOLID**, garantindo:
- Separação clara de responsabilidades
- Facilidade de manutenção e testes
- Baixo acoplamento entre camadas
- Alta coesão dentro de cada módulo

## Camadas da Aplicação

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│                     (FastAPI Routers)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  customers   │  │   payments   │  │   webhooks   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     BUSINESS LAYER                       │
│                       (Services)                         │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │  CustomerService     │  │  PaymentService      │    │
│  │  - create_customer   │  │  - create_payment    │    │
│  │  - get_customer      │  │  - get_payment       │    │
│  └──────────────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   INTEGRATION LAYER                      │
│                    (External Clients)                    │
│              ┌──────────────────────┐                   │
│              │    AsaasClient       │                   │
│              │  - create_customer   │                   │
│              │  - create_payment    │                   │
│              │  - get_pix_qrcode    │                   │
│              └──────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Asaas API    │
                    │  (External)   │
                    └───────────────┘
```

## Estrutura de Diretórios

### `/app/core/`
**Responsabilidade:** Configurações centrais e utilitários compartilhados

- `config.py`: Gerenciamento de variáveis de ambiente com Pydantic Settings
- `logging.py`: Configuração de logging estruturado

**Princípios:**
- Single Responsibility: Cada arquivo tem uma responsabilidade única
- Dependency Inversion: Configurações são injetadas, não hardcoded

### `/app/schemas/`
**Responsabilidade:** Definição de contratos de dados (DTOs)

- `customer.py`: Schemas de entrada/saída para clientes
- `payment.py`: Schemas de entrada/saída para pagamentos
- `webhook.py`: Schemas para eventos de webhook

**Princípios:**
- Validação de dados na borda do sistema
- Imutabilidade (Pydantic models)
- Type safety com Python type hints

### `/app/clients/`
**Responsabilidade:** Comunicação com APIs externas

- `asaas.py`: Cliente HTTP para integração com Asaas

**Princípios:**
- Encapsulamento da lógica de comunicação HTTP
- Tratamento centralizado de erros
- Logging de requisições
- Facilita mocking em testes

### `/app/services/`
**Responsabilidade:** Lógica de negócio da aplicação

- `customer.py`: Regras de negócio relacionadas a clientes
- `payment.py`: Regras de negócio relacionadas a pagamentos

**Princípios:**
- Orquestração entre diferentes camadas
- Transformação de dados entre schemas e APIs externas
- Validações de negócio
- Independente de framework (pode ser usado fora do FastAPI)

### `/app/routers/`
**Responsabilidade:** Definição de endpoints HTTP

- `customers.py`: Endpoints de gerenciamento de clientes
- `payments.py`: Endpoints de gerenciamento de pagamentos
- `webhooks.py`: Endpoints para receber notificações

**Princípios:**
- Thin controllers: Apenas roteamento e validação HTTP
- Delegação da lógica para services
- Tratamento de exceções HTTP
- Documentação automática (OpenAPI)

## Fluxo de Dados

### Exemplo: Criar Pagamento PIX

```
1. Cliente HTTP
   │
   ▼
2. POST /payments (Router)
   │ - Valida payload com Pydantic
   │ - Retorna 422 se inválido
   ▼
3. PaymentService.create_payment()
   │ - Aplica regras de negócio
   │ - Transforma PaymentCreateRequest em payload Asaas
   ▼
4. AsaasClient.create_payment()
   │ - Faz requisição HTTP para Asaas
   │ - Trata erros de rede/API
   │ - Retorna resposta raw
   ▼
5. PaymentService (continuação)
   │ - Se PIX, busca QR Code
   │ - Transforma resposta em PaymentResponse
   ▼
6. Router (continuação)
   │ - Retorna 201 Created
   │ - Serializa PaymentResponse como JSON
   ▼
7. Cliente HTTP recebe resposta
```

## Padrões de Design Utilizados

### 1. Repository Pattern (Implícito)
O `AsaasClient` atua como um repository, abstraindo a fonte de dados (API externa).

### 2. Service Layer Pattern
Services encapsulam a lógica de negócio, mantendo controllers magros.

### 3. DTO (Data Transfer Object)
Schemas Pydantic servem como DTOs, garantindo validação e type safety.

### 4. Dependency Injection
FastAPI injeta dependências automaticamente (pode ser expandido).

### 5. Factory Pattern
`get_settings()` usa `@lru_cache` para criar singleton de configurações.

## Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada classe/módulo tem uma única razão para mudar
- Routers: apenas roteamento HTTP
- Services: apenas lógica de negócio
- Clients: apenas comunicação externa

### Open/Closed Principle (OCP)
- Fácil adicionar novos métodos de pagamento sem modificar código existente
- Schemas podem ser estendidos via herança

### Liskov Substitution Principle (LSP)
- Schemas derivados podem substituir schemas base
- Facilita criação de mocks para testes

### Interface Segregation Principle (ISP)
- Schemas específicos para cada operação (CreateRequest, Response)
- Clientes não são forçados a depender de métodos que não usam

### Dependency Inversion Principle (DIP)
- Services dependem de abstrações (schemas), não de implementações concretas
- Configurações são injetadas via `get_settings()`

## Tratamento de Erros

### Camada de Router
```python
try:
    service = PaymentService()
    return await service.create_payment(payment)
except Exception as e:
    logger.error(f"Error: {str(e)}")
    raise HTTPException(status_code=400, detail=str(e))
```

### Camada de Client
```python
try:
    response = await client.request(...)
    response.raise_for_status()
    return response.json()
except httpx.HTTPStatusError as e:
    logger.error(f"API error: {e.response.status_code}")
    raise
```

## Segurança

### Validação de Entrada
- Pydantic valida todos os dados de entrada
- Regex para CPF/CNPJ e telefone
- EmailStr para validação de email

### Não Armazenamento de Dados Sensíveis
- Dados de cartão são enviados diretamente ao Asaas
- Não há persistência local de informações sensíveis

### Logging Seguro
- Não loga dados sensíveis (cartão, senhas)
- Logs estruturados para auditoria

### Idempotência
- Webhooks verificam eventos já processados
- Previne processamento duplicado

## Escalabilidade

### Horizontal Scaling
- Stateless: pode rodar múltiplas instâncias
- Sem dependência de estado local

### Async/Await
- Operações I/O não bloqueantes
- Melhor utilização de recursos

### Preparado para Cache
- Estrutura permite adicionar Redis facilmente
- Services podem ser decorados com cache

### Preparado para Fila
- Webhooks podem ser movidos para processamento assíncrono
- Celery/RabbitMQ podem ser integrados

## Testabilidade

### Mocking Facilitado
```python
@pytest.fixture
def mock_asaas_client(mocker):
    return mocker.patch("app.clients.asaas.AsaasClient")

def test_create_payment(mock_asaas_client):
    mock_asaas_client.return_value.create_payment.return_value = {...}
    # Test service logic
```

### Testes de Integração
```python
from fastapi.testclient import TestClient

def test_create_customer():
    response = client.post("/customers", json={...})
    assert response.status_code == 201
```

## Observabilidade

### Logging Estruturado
```python
logger.info(f"Creating payment: {payment_data.billingType}")
logger.error(f"Error creating payment: {str(e)}")
```

### Health Check
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Preparado para Métricas
- Estrutura permite adicionar Prometheus
- Middleware pode coletar métricas de requisições

## Evolução da Arquitetura

### Próximos Passos

1. **Adicionar Camada de Persistência**
   ```
   Services → Repositories → Database
   ```

2. **Implementar CQRS**
   ```
   Commands (Write) ← → Queries (Read)
   ```

3. **Event-Driven Architecture**
   ```
   Services → Event Bus → Event Handlers
   ```

4. **Microservices**
   ```
   Customer Service | Payment Service | Notification Service
   ```

## Conclusão

A arquitetura atual é:
- ✅ Simples e direta para começar
- ✅ Preparada para crescer
- ✅ Testável e manutenível
- ✅ Segue boas práticas da indústria
- ✅ Fácil de entender para novos desenvolvedores
