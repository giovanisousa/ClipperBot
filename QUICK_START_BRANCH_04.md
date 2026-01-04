# 🚀 Quick Start - Branch 04: Segurança e Licenciamento

## Resumo
Sistema de autenticação com Hardware Lock, validação de licença e tela de login.

---

## 📋 Pré-requisitos

✅ Python 3.8+  
✅ Ambiente virtual ativado  
✅ Dependências instaladas

---

## ⚡ Instalação Rápida

### 1. Instalar novas dependências

```powershell
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar Branch 04
pip install fastapi uvicorn[standard] pydantic requests pyjwt python-multipart
```

### 2. Testar instalação

```powershell
python test_branch_04.py
```

**Saída esperada:**
- ✅ HWID gerado
- ✅ Auth Client OK
- ✅ Todas as dependências instaladas

---

## 🎮 Uso

### Modo 1: Execução Automática (Recomendado)

**Terminal 1** - Servidor Mock:
```powershell
.\start_auth_server.ps1
```

**Terminal 2** - Aplicação:
```powershell
.venv\Scripts\activate
python gui_main.py
```

### Modo 2: Execução Manual

**Terminal 1** - Servidor Mock:
```powershell
.venv\Scripts\activate
python auth_server_mock.py
```

**Terminal 2** - Aplicação:
```powershell
.venv\Scripts\activate
python gui_main.py
```

---

## 🔑 Credenciais de Teste

### Usuário 1 (Demo)
- **Email:** demo@clipperbot.com
- **Senha:** demo123
- **Status:** Ativo
- **Expira:** 30 dias

### Usuário 2 (Test)
- **Email:** test@example.com
- **Senha:** test123
- **Status:** Ativo
- **Expira:** 15 dias

---

## 🎯 Fluxo de Uso

1. **Iniciar servidor mock** → `start_auth_server.ps1`
2. **Executar aplicação** → `python gui_main.py`
3. **Tela de login aparece**
4. **Digitar credenciais** → demo@clipperbot.com / demo123
5. **Clicar "Entrar"**
6. **Aplicação principal abre** com card do usuário
7. **Card mostra:**
   - ✅ Email
   - 🟢 Status (Ativo)
   - 📅 Dias restantes
   - 🚪 Botão Sair

---

## 🧪 Testes Específicos

### Teste 1: HWID Generator

```powershell
python src/hwid_generator.py
```

**Resultado:** Hash MD5 de 32 caracteres (sempre o mesmo)

### Teste 2: Tela de Login

```powershell
python src/login_window.py
```

**Resultado:** Janela de login aparece

### Teste 3: Auth Client

```powershell
python -c "from src.auth_client import AuthClient; print(AuthClient().API_BASE_URL)"
```

**Resultado:** `http://localhost:8000/api`

---

## 🐛 Problemas Comuns

### ❌ "Não foi possível conectar ao servidor"

**Causa:** Servidor mock não está rodando

**Solução:**
```powershell
.\start_auth_server.ps1
```

### ❌ "Module 'fastapi' not found"

**Causa:** Dependências não instaladas

**Solução:**
```powershell
pip install -r requirements.txt
```

### ❌ "Licença já em uso em outro computador"

**Causa:** HWID diferente detectado

**Solução:**
1. Chamar endpoint de liberação:
```powershell
curl -X POST http://localhost:8000/api/auth/release `
  -H "Content-Type: application/json" `
  -d '{"email":"demo@clipperbot.com","password":"demo123"}'
```

2. Fazer login novamente

---

## 📊 Endpoints da API

| Método | URL                          | Descrição             |
|--------|------------------------------|-----------------------|
| GET    | http://localhost:8000        | Info da API           |
| GET    | http://localhost:8000/health | Health check          |
| GET    | http://localhost:8000/docs   | Swagger UI            |
| POST   | /api/auth/login              | Login                 |
| GET    | /api/auth/validate           | Validar token         |
| POST   | /api/auth/logout             | Logout                |
| POST   | /api/auth/release            | Liberar licença       |

---

## 📚 Documentação Completa

Ver: [BRANCH_04_SECURITY.md](BRANCH_04_SECURITY.md)

---

## 🎉 Conclusão

Após seguir este guia:
- ✅ Servidor mock rodando
- ✅ Tela de login funcional
- ✅ Sistema de HWID operacional
- ✅ Validação de licença ativa
- ✅ Card de usuário na GUI

**Próximo passo:** Implementar servidor de produção real!
