#!/bin/bash

echo "🚀 ConAssas API - Setup Script"
echo "================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado"
    echo "📝 Criando .env a partir do .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais do Asaas!"
    echo "   - ASAAS_API_KEY: Sua chave de API"
    echo "   - ASAAS_BASE_URL: URL do sandbox ou produção"
    echo ""
    read -p "Pressione ENTER para continuar..."
fi

echo ""
echo "✅ Setup concluído!"
echo ""
echo "Para iniciar a API, execute:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Ou use o script de inicialização:"
echo "  ./start.sh"
echo ""
echo "Documentação disponível em:"
echo "  http://localhost:8000/docs"
