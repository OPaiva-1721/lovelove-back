# Como Testar o Banco de Dados Localmente

Este guia explica como verificar se o banco de dados PostgreSQL está funcionando corretamente quando você roda a aplicação localmente.

## 📋 Pré-requisitos

1. **PostgreSQL instalado e rodando**
2. **Arquivo `.env` configurado** (baseado no `env.example`)
3. **Ambiente virtual ativado** (`venv`)

## 🚀 Testes Disponíveis

### 1. Teste Rápido
Para um teste básico de conexão:
```bash
python quick_db_test.py
```

### 2. Teste Completo
Para um teste detalhado que verifica:
- Conexão com o banco
- Existência do banco de dados
- Tabelas criadas
- Integração com Flask

```bash
python test_database.py
```

## 🔧 Configuração do Banco

### 1. Criar o banco de dados
Se o banco `lovelove_db` não existir, crie-o:
```sql
CREATE DATABASE lovelove_db;
```

### 2. Configurar o arquivo .env
Copie o `env.example` para `.env` e ajuste as configurações:
```bash
cp env.example .env
```

### 3. Verificar configurações
O arquivo `.env` deve conter:
```env
DB_USER=postgres
DB_PASSWORD=paiva123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lovelove_db
```

## 🐛 Solução de Problemas

### Erro de Conexão
- **Verifique se o PostgreSQL está rodando**
- **Confirme as credenciais** no arquivo `.env`
- **Teste a conexão manual**:
  ```bash
  psql -U postgres -h localhost -d lovelove_db
  ```

### Banco não encontrado
- **Crie o banco**:
  ```sql
  CREATE DATABASE lovelove_db;
  ```

### Tabelas não criadas
- **Execute a aplicação** para criar as tabelas:
  ```bash
  python src/main.py
  ```

### Erro de permissão
- **Verifique se o usuário tem permissões**:
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE lovelove_db TO postgres;
  ```

## 📊 Verificação Manual

### Via PostgreSQL CLI
```bash
psql -U postgres
\c lovelove_db
\dt
```

### Via Aplicação
1. **Inicie a aplicação**:
   ```bash
   python src/main.py
   ```
2. **Acesse** `http://localhost:5000`
3. **Verifique os logs** para erros de banco

## ✅ Resultados Esperados

### Teste Rápido
```
🔍 Teste rápido do banco de dados...
✅ Banco de dados funcionando!
```

### Teste Completo
```
🚀 Iniciando testes do banco de dados...

📋 Configurações atuais:
   Host: localhost
   Porta: 5432
   Usuário: postgres
   Banco: lovelove_db

🔍 Testando conexão com o banco de dados...
✅ Conexão com o banco de dados estabelecida com sucesso!
✅ Banco de dados 'lovelove' encontrado!
✅ Conseguiu acessar o banco 'lovelove'!
✅ Encontradas 6 tabela(s): user, relationship, photo, post, message, comment

🔍 Testando aplicação Flask...
✅ Aplicação Flask consegue se conectar ao banco!
✅ Todas as tabelas esperadas foram encontradas!

🎉 Todos os testes passaram! O banco está funcionando corretamente.
```

## 🔄 Próximos Passos

Se todos os testes passarem:
1. **Inicie a aplicação**: `python src/main.py`
2. **Teste as rotas da API** no Postman ou similar
3. **Verifique se os dados estão sendo salvos** no banco

Se houver problemas:
1. **Verifique os logs** de erro
2. **Confirme as configurações** do PostgreSQL
3. **Teste a conexão manual** via PostgreSQL CLI
