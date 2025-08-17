#!/bin/bash

echo "🚀 Iniciando LoveLove..."

# Aguardar MySQL ficar pronto
echo "⏳ Aguardando MySQL..."
while ! nc -z db 3306; do
  echo "MySQL ainda não está pronto, aguardando..."
  sleep 2
done

echo "✅ MySQL está pronto!"

# Aguardar um pouco mais para garantir que o MySQL está totalmente inicializado
sleep 5

# Executar script de população de dados
echo "📊 Populando dados iniciais..."
python populate_data.py

# Iniciar aplicação
echo "🌐 Iniciando aplicação Flask..."
python run.py
