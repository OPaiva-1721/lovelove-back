# Usar Python 3.11 como base
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para uploads
RUN mkdir -p src/static/uploads

# Tornar script executável
RUN chmod +x start.sh

# Expor porta
EXPOSE 5000

# Comando para executar a aplicação
CMD ["bash", "start.sh"]
