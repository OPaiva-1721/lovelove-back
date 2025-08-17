# 🚀 Deploy no Render

Este guia explica como fazer deploy do LoveLove no Render (plataforma gratuita para Python).

## 📋 Pré-requisitos

- Conta no GitHub
- Conta no Render (gratuita)
- Código no GitHub

## 🚀 Passo a Passo

### 1. **Preparar o Código**

Certifique-se de que seu código está no GitHub com os arquivos:
- `render.yaml`
- `requirements.txt` (atualizado)
- `config.py` (atualizado)

### 2. **Criar Conta no Render**

1. Acesse: https://render.com
2. Clique em "Sign Up"
3. Faça login com GitHub

### 3. **Criar Novo Web Service**

1. Clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `lovelove_backend`

### 4. **Configurar o Serviço**

**Nome:** `lovelove-backend`
**Runtime:** `Python 3`
**Build Command:** `pip install -r requirements.txt`
**Start Command:** `gunicorn src.main:app`

### 5. **Configurar Banco de Dados**

1. Clique em "New +"
2. Selecione "PostgreSQL"
3. Nome: `lovelove-db`
4. Copie as credenciais

### 6. **Configurar Variáveis de Ambiente**

No seu Web Service, adicione:

```env
RENDER=true
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:5432/database
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=sua_chave_jwt
```

### 7. **Deploy**

1. Clique em "Create Web Service"
2. Aguarde o build (5-10 minutos)
3. Acesse a URL fornecida

## 🔧 Configuração Automática

Se você usar o arquivo `render.yaml`, o Render configurará automaticamente:
- Web Service
- Banco PostgreSQL
- Variáveis de ambiente

## 📱 URLs da API

Após o deploy, suas URLs serão:
- **API:** `https://lovelove-backend.onrender.com`
- **Relacionamento:** `https://lovelove-backend.onrender.com/api/relationship`
- **Posts:** `https://lovelove-backend.onrender.com/api/posts`
- **Mensagens:** `https://lovelove-backend.onrender.com/api/messages`

## 🔍 Troubleshooting

### **Erro de Build**
- Verifique se todas as dependências estão no `requirements.txt`
- Confirme se o Python 3.11 está sendo usado

### **Erro de Conexão com Banco**
- Verifique se o banco PostgreSQL foi criado
- Confirme as variáveis de ambiente

### **Erro de Importação**
- Verifique se o `src.main:app` está correto
- Confirme se o arquivo `src/main.py` existe

## 💡 Dicas

1. **Primeiro deploy** pode demorar 10-15 minutos
2. **Deploys subsequentes** são mais rápidos
3. **Logs** estão disponíveis no painel do Render
4. **Domínio personalizado** pode ser configurado

## 🎯 Próximos Passos

1. **Teste a API** após o deploy
2. **Configure o frontend** para usar a nova URL
3. **Monitore os logs** para identificar problemas
4. **Configure backup** do banco de dados

---

**🎉 Seu LoveLove estará online no Render!**
