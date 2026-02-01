#!/bin/bash

echo "🧪 Testes da ConAssas API"
echo "================================"
echo ""

BASE_URL="http://localhost:8000"

echo "1️⃣  Testando Health Check..."
curl -s $BASE_URL/health | python3 -m json.tool
echo ""

echo "2️⃣  Testando validação de CPF inválido (deve retornar erro 422)..."
curl -s -X POST $BASE_URL/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste",
    "cpfCnpj": "123",
    "email": "teste@example.com",
    "phone": "11999999999"
  }' | python3 -m json.tool
echo ""

echo "3️⃣  Testando validação de email inválido (deve retornar erro 422)..."
curl -s -X POST $BASE_URL/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste",
    "cpfCnpj": "12345678901",
    "email": "email-invalido",
    "phone": "11999999999"
  }' | python3 -m json.tool
echo ""

echo "4️⃣  Testando validação de pagamento sem dados de cartão..."
curl -s -X POST $BASE_URL/payments \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_test",
    "value": 100.00,
    "billingType": "CREDIT_CARD",
    "dueDate": "2026-02-15"
  }' | python3 -m json.tool
echo ""

echo "✅ Testes de validação concluídos!"
echo ""
echo "⚠️  Para testar com dados reais do Asaas:"
echo "   1. Configure sua API Key no arquivo .env"
echo "   2. Execute: ./start.sh"
echo "   3. Use os exemplos em EXAMPLES.md"
