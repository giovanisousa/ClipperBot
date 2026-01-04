# ⚡ Quick Start - Branch 04 (Desenvolvimento Local)

## 🚀 Teste Rápido da Branch 04

### 1️⃣ Instalar Dependências

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências da Branch 04
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary pyjwt python-multipart pydantic
```

### 2️⃣ Iniciar Servidor Mock (Desenvolvimento Local)

```bash
# Terminal 1: Servidor de autenticação MOCK
python auth_server_mock.py
```

**Saída esperada:**
```
🚀 ClipperBot Auth API (MOCK) - Iniciando...
📋 Usuários de teste:
  • demo@clipperbot.com
    Senha: demo123
  • test@example.com
    Senha: test123
🌐 API disponível em: http://localhost:8000
📚 Documentação: http://localhost:8000/docs
```

### 3️⃣ Testar Desktop App

```bash
# Terminal 2: Aplicação desktop
python gui_main.py
```

**Fazer login com:**
- Email: `demo@clipperbot.com`
- Senha: `demo123`

✅ **Sucesso:** Você verá a GUI principal com o card do usuário no topo!

---

## 🧪 Testes Disponíveis

### Teste 1: Estrutura do Backend
```bash
python test_backend_production.py
```

### Teste 2: HWID Generator
```bash
python -c "from src.hwid_generator import HardwareIDGenerator; print(HardwareIDGenerator.generate_hwid())"
```

### Teste 3: Auth Client
```bash
python src/auth_client.py
```

### Teste 4: Login Window
```bash
python src/login_window.py
```

---

## 📚 Documentação da API Mock

Acesse no navegador após iniciar o servidor mock:

```
http://localhost:8000/docs
```

Endpoints disponíveis:
- `POST /api/auth/login` - Fazer login
- `GET /api/auth/validate` - Validar token
- `POST /api/auth/logout` - Logout
- `POST /api/auth/release` - Liberar licença
- `POST /api/webhooks/kiwify` - Webhook Kiwify

---

## 🔧 Problemas Comuns

### ❌ ModuleNotFoundError: No module named 'fastapi'
**Solução:** `pip install fastapi uvicorn[standard]`

### ❌ Connection refused (Desktop App)
**Solução:** Certifique-se de que o servidor mock está rodando (`python auth_server_mock.py`)

### ❌ Login falha com "hardware_mismatch"
**Solução:** 
1. No servidor mock, delete o usuário
2. Ou use `POST /api/auth/release` para liberar a licença

---

## 🌐 Próximo Passo: Deploy em Produção

Quando estiver pronto para produção, siga:

📖 **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**

Passos:
1. Criar conta no Neon.tech (PostgreSQL)
2. Criar conta no Render.com (API Hosting)
3. Configurar variáveis de ambiente
4. Deploy automático via GitHub

---

## 📊 Comparação: Mock vs Produção

| Recurso | Mock (Local) | Produção (Cloud) |
|---------|--------------|------------------|
| Banco de dados | Memória (RAM) | PostgreSQL (Neon.tech) |
| Persistência | ❌ Perdido ao reiniciar | ✅ Permanente |
| HTTPS | ❌ HTTP local | ✅ HTTPS com SSL |
| Usuários | 2 pré-definidos | Ilimitados (Kiwify) |
| Performance | Instantâneo | ~100-300ms |
| Custo | $0 | $0 (Free Tier) |

---

## ✅ Checklist de Validação

Antes de fazer deploy em produção, valide:

- [ ] Servidor mock funciona localmente
- [ ] Desktop app consegue fazer login
- [ ] HWID é gerado corretamente
- [ ] Token JWT é salvo e persistido
- [ ] Auto-login funciona após fechar/abrir app
- [ ] Logout limpa sessão
- [ ] Hardware lock bloqueia segundo PC
- [ ] Tela de login é exibida primeiro

---

## 🎓 Comandos Úteis

```bash
# Ver logs do servidor mock
# (Terminal onde rodou: python auth_server_mock.py)

# Testar endpoint manualmente (PowerShell)
$body = @{email="demo@clipperbot.com"; password="demo123"; hwid="test123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method POST -Body $body -ContentType "application/json"

# Verificar token salvo
cat ~/.clipperbot/session.json

# Limpar sessão
rm ~/.clipperbot/session.json
```
