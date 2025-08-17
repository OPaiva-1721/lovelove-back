# 💕 LoveLove - Rede Social para Casais

Uma rede social especial para você e sua namorada compartilharem momentos especiais!

## 🚀 Como Usar

### 🐳 **Opção 1: Com Docker (Recomendado)**

1. **Instale o Docker Desktop**
2. **Execute o projeto:**
   ```bash
   docker-compose up --build
   ```
3. **Acesse:** http://localhost:5000

### 💻 **Opção 2: Instalação Local**

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure o banco MySQL:**
   - Crie um banco chamado `lovelove`
   - Configure as variáveis no `config.py`

3. **Execute:**
   ```bash
   python populate_data.py
   python run.py
   ```

## 🌐 **Deploy em Produção**

### 🚀 **Render (Recomendado - Gratuito)**

1. **Faça push do código para GitHub**
2. **Acesse:** https://render.com
3. **Crie uma conta gratuita**
4. **Siga o guia:** [DEPLOY.md](DEPLOY.md)

**URLs após deploy:**
- API: `https://lovelove-backend.onrender.com`
- Relacionamento: `https://lovelove-backend.onrender.com/api/relationship`
- Posts: `https://lovelove-backend.onrender.com/api/posts`

### 🐳 **Docker em Produção**

```bash
# Produção
docker-compose -f docker-compose.yml up -d

# Desenvolvimento
docker-compose up --build
```

## 📋 **Registro de Usuários**

### 1. **Registro de Usuários**
Primeiro, vocês precisam se registrar:

**Para você:**
```bash
POST /api/auth/register
{
    "username": "Gabryel",
    "email": "gabryel@email.com",
    "password": "sua_senha"
}
```

**Para sua namorada:**
```bash
POST /api/auth/register
{
    "username": "Amabilly",
    "email": "amabilly@email.com",
    "password": "senha_dela"
}
```

### 2. **Login**
Depois do registro, façam login:

```bash
POST /api/auth/login
{
    "email": "seu_email@email.com",
    "password": "sua_senha"
}
```

### 3. **Ver Usuários**
Para ver os IDs de vocês:

```bash
GET /api/users
```

### 4. **Enviar Mensagens**
Para enviar mensagens um para o outro:

```bash
POST /api/messages/simple
{
    "sender_id": 1,
    "recipient_id": 2,
    "content": "Oi amor! Te amo! ❤️"
}
```

### 5. **Ver Mensagens**
Para ver todas as mensagens:

```bash
GET /api/messages
```

## 📱 Funcionalidades

- ✅ **Registro e Login** - Sistema de autenticação seguro
- ✅ **Mensagens Privadas** - Conversas entre vocês
- ✅ **Posts** - Compartilhar momentos especiais
- ✅ **Fotos** - Upload de fotos do casal
- ✅ **Relacionamento** - Contador de dias juntos
- ✅ **Likes e Comentários** - Interação nos posts

## 🔧 Configuração para Deploy

### 🚀 **Render (Gratuito):**
```bash
# 1. Push para GitHub
git add .
git commit -m "Deploy ready"
git push

# 2. Conectar no Render
# 3. Deploy automático
```

### 🐳 **Docker:**
```bash
# Produção
docker-compose -f docker-compose.yml up -d

# Desenvolvimento
docker-compose up --build
```

### 💻 **Instalação Local:**

#### Variáveis de Ambiente:
```bash
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_HOST=localhost
DB_NAME=lovelove
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=sua_chave_jwt
```

#### Banco de Dados:
1. Crie um banco MySQL chamado `lovelove`
2. Execute `python populate_data.py` para criar dados iniciais
3. Execute `python run.py` para iniciar o servidor

## 💡 Dicas de Uso

1. **Segurança**: Use senhas fortes
2. **Backup**: Faça backup regular do banco de dados
3. **Fotos**: As fotos ficam salvas em `src/static/uploads/`
4. **Tokens**: Guarde os tokens JWT para autenticação

## 🎯 Próximos Passos

- [ ] Notificações em tempo real
- [ ] Emojis e stickers
- [ ] Calendário de eventos
- [ ] Lista de desejos compartilhada
- [ ] Músicas favoritas do casal

## 📚 Documentação Adicional

- [Docker Guide](DOCKER.md) - Guia completo para Docker
- [Deploy Guide](DEPLOY.md) - Guia de deploy no Render
- [API Documentation](API.md) - Documentação da API

---

**Desenvolvido com ❤️ para casais apaixonados!**
