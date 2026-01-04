# 🚀 Guia de Deploy - ClipperBot Auth API

## Arquitetura de Produção

```
┌─────────────────┐
│  Desktop App    │
│  (Windows/Mac)  │
└────────┬────────┘
         │
         │ HTTPS
         ▼
┌─────────────────┐
│  Render.com     │◄─── API de Autenticação (FastAPI)
│  (API Server)   │
└────────┬────────┘
         │
         │ PostgreSQL
         ▼
┌─────────────────┐
│  Neon.tech      │◄─── Banco de Dados (PostgreSQL)
│  (Database)     │
└─────────────────┘
```

## Passo 1: Configurar Banco de Dados (Neon.tech)

### 1.1 Criar Conta no Neon.tech
1. Acesse: https://neon.tech
2. Crie conta gratuita
3. Crie novo projeto: "clipperbot-db"

### 1.2 Obter Connection String
1. No dashboard, clique em "Connection Details"
2. Copie a **Connection String** (formato PostgreSQL)
3. Exemplo: `postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/clipperbot?sslmode=require`

### 1.3 Inicializar Banco
```bash
# Criar arquivo .env local
cp .env.example .env

# Editar .env e adicionar DATABASE_URL
# DATABASE_URL=postgresql://seu-usuario:sua-senha@ep-xxxxx.neon.tech/clipperbot?sslmode=require

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco (criar tabelas + admin)
python backend/init_db.py
```

**Resultado esperado:**
```
✅ Tabelas criadas com sucesso
✅ Usuário admin criado com sucesso
   Email: admin@clipperbot.com
   Senha: admin123
```

---

## Passo 2: Deploy no Render.com

### 2.1 Criar Conta no Render
1. Acesse: https://render.com
2. Faça login com GitHub
3. Autorize acesso ao repositório do ClipperBot

### 2.2 Criar Web Service
1. Dashboard → **New +** → **Web Service**
2. Conecte seu repositório GitHub
3. Configurações:

```yaml
Name: clipperbot-auth-api
Region: Oregon (US West)
Branch: feature/security-licensing
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn backend.api:app --host 0.0.0.0 --port $PORT
```

### 2.3 Configurar Environment Variables
No Render, adicione as variáveis:

```bash
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/clipperbot?sslmode=require
JWT_SECRET_KEY=<gerar-chave-segura>
ENVIRONMENT=production
```

**Gerar JWT_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Deploy
1. Clique em **Create Web Service**
2. Aguarde deploy (2-3 minutos)
3. URL final: `https://clipperbot-auth-api.onrender.com`

### 2.5 Testar API
```bash
# Health check
curl https://clipperbot-auth-api.onrender.com/health

# Documentação interativa
# Abra no navegador: https://clipperbot-auth-api.onrender.com/docs
```

---

## Passo 3: Configurar Desktop App

### 3.1 Atualizar URL da API
Edite `src/auth_client.py`:

```python
# Trocar de:
API_BASE_URL = "http://localhost:8000/api"

# Para:
API_BASE_URL = "https://clipperbot-auth-api.onrender.com/api"
```

### 3.2 Testar Login
```bash
# Executar aplicação
python gui_main.py

# Fazer login com usuário admin
Email: admin@clipperbot.com
Senha: admin123
```

---

## Passo 4: Integração Kiwify (Opcional)

### 4.1 Configurar Webhook
1. Login no Kiwify
2. Produto → Configurações → Webhooks
3. Adicione URL: `https://clipperbot-auth-api.onrender.com/api/webhooks/kiwify`
4. Eventos:
   - ✅ order.approved
   - ✅ subscription.cancelled
   - ✅ subscription.renewed

### 4.2 Testar Webhook
Use ferramenta como **Webhook.site** para capturar payload do Kiwify e testar localmente.

---

## Monitoramento e Logs

### Ver Logs no Render
1. Dashboard → clipperbot-auth-api
2. **Logs** → Ver logs em tempo real

### Métricas
- **CPU/Memory**: Render dashboard
- **Database**: Neon.tech dashboard
- **Uptime**: Render (free tier dorme após inatividade)

---

## Solução de Problemas

### ❌ Erro: "Connection refused"
**Solução:** Verificar se DATABASE_URL está correto no Render

### ❌ Erro: "Table doesn't exist"
**Solução:** Executar `python backend/init_db.py` novamente

### ❌ Desktop App: "Connection Error"
**Solução:** 
1. Verificar URL da API em `auth_client.py`
2. Verificar se API está online: `curl https://seu-dominio.onrender.com/health`

### ❌ Render: "Deployment Failed"
**Solução:**
1. Verificar logs do build
2. Garantir que `requirements.txt` tem todas as dependências
3. Verificar se `PORT` variável está sendo usada

---

## Custos Estimados

| Serviço | Plano | Custo/Mês |
|---------|-------|-----------|
| Neon.tech | Free Tier | $0 (até 3 projetos) |
| Render.com | Free Tier | $0 (com limitações*) |
| **Total** | - | **$0** |

\* **Limitações Free Tier Render:**
- Serviço "dorme" após 15 min de inatividade
- Primeiro request após dormir demora ~30s
- 750h/mês de uso

**Upgrade recomendado (Starter $7/mês):**
- Sempre online (sem sleep)
- Deploy mais rápido
- Melhor performance

---

## Próximos Passos

1. ✅ Configurar domínio customizado (ex: api.clipperbot.com)
2. ✅ Implementar rate limiting (proteção contra ataques)
3. ✅ Adicionar admin panel para gerenciar usuários
4. ✅ Configurar backup automático do banco (Neon.tech)
5. ✅ Implementar logs estruturados (Sentry, Datadog)

---

## Suporte

- **Neon.tech Docs:** https://neon.tech/docs
- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
