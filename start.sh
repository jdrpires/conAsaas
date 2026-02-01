#!/bin/bash

echo "🚀 Iniciando ConAssas API..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute ./setup.sh primeiro"
    exit 1
fi

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado. Execute ./setup.sh primeiro"
    exit 1
fi

# Iniciar servidor
echo "✅ Iniciando servidor na porta 8000..."
echo "📚 Documentação: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
