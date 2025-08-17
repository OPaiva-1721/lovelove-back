# 🐳 LoveLove com Docker

Este guia explica como executar o projeto LoveLove usando Docker.

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose instalado

## 🚀 Como Executar

### 1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd lovelove_backend
```

### 2. **Execute com Docker Compose**
```bash
docker-compose up --build
```

### 3. **Acesse a aplicação**
- API: http://localhost:5000
- Banco MySQL: localhost:3306

## 🔧 Comandos Úteis

### **Iniciar em background**
```bash
docker-compose up -d --build
```

### **Ver logs**
```bash
docker-compose logs -f app
```

### **Parar serviços**
```bash
docker-compose down
```

### **Parar e remover volumes**
```bash
docker-compose down -v
```

### **Reconstruir apenas a aplicação**
```bash
docker-compose build app
```

## 📁 Estrutura dos Containers

### **Container `lovelove_app`**
- Porta: 5000
- Volume: `./src/static/uploads` (fotos)
- Dependências: MySQL

### **Container `lovelove_mysql`**
- Porta: 3306
- Volume: `mysql_data` (dados persistentes)
- Senha root: `paiva123`

## 🔐 Variáveis de Ambiente

As variáveis estão configuradas no `docker-compose.yml`:

```yaml
environment:
  - DB_USER=root
  - DB_PASSWORD=paiva123
  - DB_HOST=db
  - DB_PORT=3306
  - DB_NAME=lovelove
  - SECRET_KEY=lovelove#secret$key$2024
  - JWT_SECRET_KEY=lovelove.jwt.secret.2024
```

## 📊 Dados Iniciais

O script `populate_data.py` é executado automaticamente na inicialização, criando:
- Usuários de exemplo
- Relacionamento inicial
- Posts de exemplo
- Mensagens de exemplo

## 🖼️ Upload de Fotos

As fotos são salvas em:
- **Host**: `./src/static/uploads/`
- **Container**: `/app/src/static/uploads/`

## 🔍 Troubleshooting

### **Problema: MySQL não conecta**
```bash
# Verificar se o MySQL está rodando
docker-compose logs db

# Reiniciar apenas o banco
docker-compose restart db
```

### **Problema: Aplicação não inicia**
```bash
# Verificar logs da aplicação
docker-compose logs app

# Reconstruir container
docker-compose build --no-cache app
```

### **Problema: Porta já em uso**
```bash
# Verificar portas em uso
netstat -tulpn | grep :5000

# Parar outros serviços
docker-compose down
```

## 🚀 Deploy em Produção

### **1. Configurar variáveis de ambiente**
Crie um arquivo `.env`:
```env
DB_PASSWORD=sua_senha_segura
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=sua_chave_jwt
```

### **2. Usar volumes externos**
```yaml
volumes:
  mysql_data:
    external: true
  uploads:
    external: true
```

### **3. Configurar proxy reverso**
Use Nginx ou Traefik para HTTPS.

## 📝 Logs

### **Ver logs em tempo real**
```bash
docker-compose logs -f
```

### **Ver logs de um serviço específico**
```bash
docker-compose logs -f app
docker-compose logs -f db
```

## 🧹 Limpeza

### **Remover containers e volumes**
```bash
docker-compose down -v
```

### **Remover imagens**
```bash
docker rmi lovelove_backend_app
docker rmi mysql:8.0
```

---

**🎉 Agora você pode executar o LoveLove com Docker!**
