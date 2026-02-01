import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "ConAssas API" in response.json()["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_customer_validation():
    # Teste com CPF inválido
    response = client.post("/customers", json={
        "name": "Test User",
        "cpfCnpj": "123",  # CPF inválido
        "email": "test@example.com",
        "phone": "11999999999"
    })
    assert response.status_code == 422


def test_create_payment_validation():
    # Teste sem dados de cartão quando billingType é CREDIT_CARD
    response = client.post("/payments", json={
        "customer_id": "cus_test",
        "value": 100.00,
        "billingType": "CREDIT_CARD",
        "dueDate": "2026-02-15"
    })
    assert response.status_code == 422


def test_webhook_idempotency():
    payload = {
        "event": "PAYMENT_CONFIRMED",
        "payment": {
            "id": "pay_test_123",
            "value": 100.00,
            "status": "CONFIRMED"
        }
    }
    
    # Primeira chamada
    response1 = client.post("/webhooks/asaas", json=payload)
    assert response1.status_code == 200
    
    # Segunda chamada (idempotente)
    response2 = client.post("/webhooks/asaas", json=payload)
    assert response2.status_code == 200
    assert response2.json()["received"] == True
