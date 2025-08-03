#!/bin/bash

echo "🚀 Iniciando WDespachante Blog System"
echo "======================================"

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se as dependências estão instaladas
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não instaladas!"
    echo "Execute: pip install -r requirements.txt"
    exit 1
fi

# Mostrar configurações
echo "📊 Configurações do Sistema:"
python -c "
from app import app
print(f'   - Limite de vídeo: {app.config.get(\"MAX_VIDEO_SIZE\", 0) // (1024*1024)}MB')
print(f'   - Limite geral: {app.config.get(\"MAX_CONTENT_LENGTH\", 0) // (1024*1024)}MB')
print(f'   - Formatos de vídeo: {app.config.get(\"ALLOWED_VIDEO_EXTENSIONS\", \"N/A\")}')
"

echo ""
echo "🌐 URLs do Sistema:"
echo "   - Site principal: http://localhost:5000"
echo "   - Painel admin: http://localhost:5000/admin"
echo "   - Login: admin / admin"
echo ""
echo "⚡ Iniciando servidor Flask..."
echo "   Pressione Ctrl+C para parar"
echo ""

# Executar servidor
python run_server.py