# conAsaas

> FastAPI integration service for customers, charges and payment events through Asaas.

**Python · FastAPI · Pydantic · httpx · Pix · Boleto · Credit Card · Webhooks**

| | |
|---|---|
| **Type** | Payment integration API |
| **Domain** | Fintech / Payments |
| **Focus** | Provider isolation, payment orchestration and webhooks |
| **Status** | Public technical project |

## Overview

conAsaas demonstrates a clean integration boundary between an application and a payment provider. The API normalizes customer and payment operations while keeping provider communication behind a dedicated client/service layer.

## Architecture

```text
Business Application
        │
        ▼
     FastAPI
  ┌─────┼─────┐
  │     │     │
Customers Payments Webhooks
  │     │     │
  └─────┼─────┘
        ▼
   Asaas Client
        │
        ▼
    Asaas API
```

## Capabilities

- Create individual and business customers.
- Create Pix, boleto and credit-card charges.
- Support installment parameters for card payments.
- Receive payment-status webhooks.
- Validate request/response models with Pydantic.
- Async provider communication with httpx.
- Structured logging and explicit error handling.

## Quick start

```bash
git clone https://github.com/jdrpires/conAsaas.git
cd conAsaas

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
uvicorn app.main:app --reload
```

Example configuration:

```env
ASAAS_API_KEY=<your-sandbox-key>
ASAAS_BASE_URL=https://sandbox.asaas.com/api/v3
ENVIRONMENT=development
LOG_LEVEL=INFO
```

Never commit real payment-provider credentials.

## Main API surface

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/customers` | Create a customer |
| `GET` | `/customers/{customer_id}` | Retrieve a customer |
| `POST` | `/payments` | Create a charge |
| `GET` | `/payments/{payment_id}` | Retrieve payment state |
| `POST` | `/webhooks/asaas` | Receive provider events |

Swagger, ReDoc and health endpoints are available at `/docs`, `/redoc` and `/health`.

## Engineering considerations

A production payment integration should treat provider credentials, webhook authenticity, idempotency and sensitive payment data as first-class security concerns. This project keeps card handling provider-oriented and is structured so authentication, persistence and stronger webhook verification can be added without coupling them to route handlers.

## Project structure

```text
app/
├── clients/       # External provider client
├── core/          # Configuration and logging
├── routers/       # HTTP endpoints
├── schemas/       # Pydantic contracts
├── services/      # Application logic
└── main.py
```

## Why this project is public

This repository is part of my public engineering portfolio and demonstrates fintech integration, API boundaries, asynchronous HTTP communication and payment workflow design.

---

**Jean Pires** · [GitHub](https://github.com/jdrpires) · [Portfolio](https://github.com/jdrpires/jdrpires)
