# Branch 04: Sistema de Segurança e Licenciamento

## 📋 Sumário da Implementação

### Objetivo
Implementar sistema de autenticação e proteção de licença com Hardware Lock (HWID), validação de assinatura e integração com webhook Kiwify.

### Status: ✅ **IMPLEMENTADO (Versão Mock para Testes)**

---

## 🏗️ Arquitetura Implementada

### Componentes Criados

```
src/
├── hwid_generator.py      # Gerador de Hardware ID
├── auth_client.py         # Cliente de autenticação (API)
└── login_window.py        # Tela de login (CustomTkinter)

auth_server_mock.py        # Servidor API Mock (FastAPI)
gui_main.py                # Modificado: integração com autenticação
requirements.txt           # Atualizado: novas dependências
```

---

## 🔐 Módulo 1: Hardware ID Generator

**Arquivo:** `src/hwid_generator.py`

### Funcionalidade
- Gera identificador único e **consistente** da máquina
- Suporta: **Windows**, Linux e macOS
- Combina: CPU Serial + Motherboard Serial + Disk Serial
- Retorna: Hash MD5 (32 caracteres fixos)

### Uso

```python
from src.hwid_generator import HardwareIDGenerator

# Gerar HWID
hwid = HardwareIDGenerator.generate_hwid()
print(hwid)  # Ex: "a3f7b9c1e2d4f5a6b7c8d9e0f1a2b3c4"

# Verificar HWID
is_valid = HardwareIDGenerator.verify_hwid(stored_hwid)
```

### Comandos Windows Utilizados
- `wmic cpu get ProcessorId`
- `wmic baseboard get SerialNumber`
- `wmic diskdrive get SerialNumber`

### Fallback
Se comandos falharem: `hostname + username + node`

---

## 🌐 Módulo 2: Authentication Client

**Arquivo:** `src/auth_client.py`

### Funcionalidade
- Comunicação com API de autenticação
- Gerenciamento de JWT tokens
- Persistência de sessão (7 dias)
- Tratamento de erros HTTP

### Endpoints Utilizados

| Método | Endpoint              | Descrição                     |
|--------|-----------------------|-------------------------------|
| POST   | `/api/auth/login`     | Login com email/senha/HWID    |
| GET    | `/api/auth/validate`  | Validação de token JWT        |
| POST   | `/api/auth/logout`    | Logout e invalidação de token |
| POST   | `/api/auth/release`   | Liberação de licença (HWID)   |

### Códigos HTTP Tratados

- **200**: Login bem-sucedido
- **401**: Credenciais inválidas
- **403**: Conta inativa ou expirada
- **409**: Licença já em uso em outro PC

### Uso

```python
from src.auth_client import AuthClient, AuthenticationError

client = AuthClient()

try:
    result = client.login("user@example.com", "senha123", hwid)
    print(f"Token: {result['access_token']}")
    print(f"Usuário: {result['user']}")
except AuthenticationError as e:
    print(f"Erro: {e}")
```

### Persistência de Sessão
- Arquivo: `~/.clipperbot/session.json`
- Validade: 7 dias
- Auto-login na próxima inicialização

---

## 🖥️ Módulo 3: Login Window

**Arquivo:** `src/login_window.py`

### Funcionalidade
- Interface gráfica de login (CustomTkinter)
- Validação de credenciais
- Feedback visual (progress bar)
- Auto-login com sessão salva
- Links: Esqueci senha / Criar conta

### Interface

```
┌──────────────────────────────────┐
│      🎬 ClipperBot               │
│   Sistema de Cortes Inteligentes │
├──────────────────────────────────┤
│ Fazer Login                      │
│                                  │
│ Email:                           │
│ [____________________________]   │
│                                  │
│ Senha:                           │
│ [____________________________]   │
│                                  │
│ [        Entrar        ]         │
│ ──────────────────────────────   │
│ Esqueci senha | Criar conta      │
│                                  │
│ Hardware ID: a3f7b9c1...         │
└──────────────────────────────────┘
```

### Uso Standalone

```python
from src.login_window import show_login

# Mostrar tela de login
user_data = show_login()

if user_data:
    print(f"✅ Autenticado: {user_data['email']}")
else:
    print("❌ Login cancelado")
```

### Threading
Login executa em **thread separada** para não bloquear UI

---

## 🚀 Módulo 4: Mock Auth Server (FastAPI)

**Arquivo:** `auth_server_mock.py`

### ⚠️ ATENÇÃO: Este é um servidor MOCK para desenvolvimento!

### Usuários de Teste

| Email                  | Senha    | Status  | Expira em |
|------------------------|----------|---------|-----------|
| demo@clipperbot.com    | demo123  | active  | 30 dias   |
| test@example.com       | test123  | active  | 15 dias   |

### Endpoints Implementados

#### 1. POST /api/auth/login

**Request:**
```json
{
  "email": "demo@clipperbot.com",
  "password": "demo123",
  "hwid": "a3f7b9c1e2d4f5a6b7c8d9e0f1a2b3c4"
}
```

**Response (200):**
```json
{
  "access_token": "xyz123...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "demo@clipperbot.com",
    "status": "active",
    "expiration_date": "2024-02-15T10:30:00",
    "created_at": "2024-01-01T08:00:00"
  }
}
```

**Validações:**
1. ✅ Email e senha corretos
2. ✅ Status da conta (active/inactive)
3. ✅ Data de expiração
4. ✅ Hardware ID (1-PC-Lock)

#### 2. GET /api/auth/validate

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "valid": true,
  "email": "demo@clipperbot.com",
  "expires_at": "2024-02-08T10:30:00"
}
```

#### 3. POST /api/auth/release

**Request:**
```json
{
  "email": "demo@clipperbot.com",
  "password": "demo123"
}
```

**Response (200):**
```json
{
  "message": "Licença liberada com sucesso",
  "email": "demo@clipperbot.com"
}
```

**Efeito:** HWID do usuário é limpo (permite login em outro PC)

#### 4. POST /api/webhooks/kiwify

**Eventos Tratados:**
- `order.approved`: Nova venda
- `subscription.cancelled`: Cancelamento
- `subscription.renewed`: Renovação

### Iniciar Servidor

```bash
# Método 1: Python direto
python auth_server_mock.py

# Método 2: Uvicorn
uvicorn auth_server_mock:app --reload
```

**URLs:**
- API: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

## 🎨 Módulo 5: Integração com GUI Principal

**Arquivo:** `gui_main.py` (modificado)

### Alterações Implementadas

1. **Import de módulos de segurança:**
```python
from src.login_window import show_login
from src.auth_client import AuthClient
```

2. **Construtor modificado:**
```python
def __init__(self, user_data: dict):
    self.user_data = user_data  # Dados do usuário autenticado
    self.auth_client = AuthClient()
    # ... resto do código
```

3. **Card de informações do usuário no sidebar:**
- Email do usuário
- Status da licença (🟢 Ativo, 🔴 Inativo, ⚠️ Expirado)
- Data de expiração (dias restantes)
- Botão de logout

4. **Fluxo de autenticação no main():**
```python
if __name__ == "__main__":
    # 1. Mostrar tela de login
    user_data = show_login()
    
    if user_data:
        # 2. Iniciar app com usuário autenticado
        app = ClipperBotGUI(user_data)
        app.run()
    else:
        # 3. Login cancelado - encerrar
        sys.exit(0)
```

### Ajustes no Layout
- Sidebar: ajustado `grid_rowconfigure` para comportar novo card
- Todas as seções reposicionadas (row +1)

---

## 📦 Novas Dependências

### Adicionadas ao requirements.txt

```txt
# Branch 04: Security & Licensing
fastapi>=0.109.0          # Framework web para API
uvicorn[standard]>=0.27.0 # Servidor ASGI
pydantic>=2.5.0           # Validação de dados
requests>=2.31.0          # Cliente HTTP
pyjwt>=2.8.0              # JWT tokens
python-multipart>=0.0.6   # Upload de arquivos
```

### Instalar Dependências

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar novas dependências
pip install fastapi uvicorn[standard] pydantic requests pyjwt python-multipart
```

---

## 🧪 Como Testar

### 1. Iniciar Servidor Mock

Em um terminal:
```bash
cd "C:\Users\Giovani Souza\Documents\ClipperBot\ClipperBot"
.venv\Scripts\activate
python auth_server_mock.py
```

**Saída esperada:**
```
==================================================
🚀 ClipperBot Auth API (MOCK) - Iniciando...
==================================================

📋 Usuários de teste:
  • demo@clipperbot.com
    Senha: demo123
    Status: active
    Expira: 2024-02-15

  • test@example.com
    Senha: test123
    Status: active
    Expira: 2024-02-01

🌐 API disponível em: http://localhost:8000
📚 Documentação: http://localhost:8000/docs
==================================================
```

### 2. Testar HWID Generator

Em outro terminal:
```bash
cd "C:\Users\Giovani Souza\Documents\ClipperBot\ClipperBot"
.venv\Scripts\activate
python src/hwid_generator.py
```

**Saída esperada:**
```
🔐 Testando Gerador de Hardware ID

Hardware ID: a3f7b9c1e2d4f5a6b7c8d9e0f1a2b3c4
Tamanho: 32 caracteres

Segunda geração: a3f7b9c1e2d4f5a6b7c8d9e0f1a2b3c4
Consistente: ✅ SIM

Verificação: ✅ PASSOU
```

### 3. Testar Tela de Login

```bash
cd "C:\Users\Giovani Souza\Documents\ClipperBot\ClipperBot"
.venv\Scripts\activate
python src/login_window.py
```

1. Digite: `demo@clipperbot.com`
2. Senha: `demo123`
3. Clique em **Entrar**

**Resultado esperado:**
✅ Mensagem "Bem-vindo(a), demo@clipperbot.com!"
✅ Janela fecha automaticamente

### 4. Executar Aplicação Completa

**IMPORTANTE:** Servidor mock deve estar rodando!

```bash
cd "C:\Users\Giovani Souza\Documents\ClipperBot\ClipperBot"
.venv\Scripts\activate
python gui_main.py
```

**Fluxo completo:**
1. ✅ Tela de login aparece
2. ✅ Digite credenciais (demo@clipperbot.com / demo123)
3. ✅ Clique "Entrar"
4. ✅ Aplicação principal abre com card do usuário
5. ✅ Sidebar mostra: email, status, dias restantes
6. ✅ Botão "Sair" disponível

---

## 🔒 Segurança Implementada

### 1. Hardware Lock (HWID)

**Como funciona:**
1. Primeiro login: HWID é **registrado** no servidor
2. Próximos logins: HWID é **validado**
3. Se diferente: **HTTP 409 Conflict**

**Proteção:**
- 1 licença = 1 PC
- Impossível usar em múltiplos computadores simultaneamente

### 2. Validação de Sessão

**Camadas de verificação:**
1. ✅ Email e senha corretos
2. ✅ Status da conta (active/inactive)
3. ✅ Data de expiração
4. ✅ Hardware ID corresponde

**Persistência:**
- Token JWT salvo localmente
- Validade: 7 dias
- Auto-login na próxima execução

### 3. Tratamento de Erros

| Cenário                          | Código | Mensagem                                |
|----------------------------------|--------|-----------------------------------------|
| Credenciais inválidas            | 401    | Email ou senha inválidos                |
| Conta inativa                    | 403    | Conta inativa. Contate suporte          |
| Assinatura expirada              | 403    | Sua assinatura expirou. Renove          |
| Licença em uso (outro PC)        | 409    | Licença já em uso em outro computador   |
| Sem conexão com servidor         | -      | Não foi possível conectar ao servidor   |

---

## 📊 Fluxograma de Autenticação

```
┌─────────────────┐
│   Iniciar App   │
└────────┬────────┘
         │
         v
┌─────────────────┐      Sim     ┌──────────────┐
│ Sessão válida?  ├──────────────>│  Auto-Login  │
└────────┬────────┘               └──────┬───────┘
         │ Não                            │
         v                                │
┌─────────────────┐                       │
│ Mostrar Login   │                       │
└────────┬────────┘                       │
         │                                │
         v                                │
┌─────────────────┐      Não     ┌──────┴───────┐
│ Credenciais OK? ├──────────────>│  Erro/Sair   │
└────────┬────────┘               └──────────────┘
         │ Sim
         v
┌─────────────────┐      Não     ┌──────────────┐
│ Status Active?  ├──────────────>│  HTTP 403    │
└────────┬────────┘               └──────────────┘
         │ Sim
         v
┌─────────────────┐      Sim     ┌──────────────┐
│   Expirado?     ├──────────────>│  HTTP 403    │
└────────┬────────┘               └──────────────┘
         │ Não
         v
┌─────────────────┐      Não     ┌──────────────┐
│ HWID Match?     ├──────────────>│  HTTP 409    │
└────────┬────────┘               └──────────────┘
         │ Sim
         v
┌─────────────────┐
│  Salvar Token   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Iniciar GUI   │
└─────────────────┘
```

---

## 🚧 Próximos Passos (Produção)

### 1. Banco de Dados Real
- [ ] SQLAlchemy + PostgreSQL/MySQL
- [ ] Tabela `users` com todos os campos
- [ ] Migração de dados (Alembic)

### 2. JWT Tokens Real
- [ ] Implementar PyJWT com secret key
- [ ] Refresh tokens (renovação automática)
- [ ] Expiração configurável

### 3. Webhook Kiwify Real
- [ ] Validação de assinatura (HMAC)
- [ ] Processamento de eventos
- [ ] Log de transações

### 4. Deploy da API
- [ ] Servidor em cloud (AWS/Azure/Heroku)
- [ ] HTTPS com certificado SSL
- [ ] Load balancer e escalabilidade

### 5. Admin Panel
- [ ] Dashboard web para gerenciar usuários
- [ ] Visualizar licenças ativas
- [ ] Reset manual de HWID

---

## 🐛 Troubleshooting

### Problema: "Não foi possível conectar ao servidor"

**Solução:**
1. Verificar se servidor mock está rodando
2. Testar: `curl http://localhost:8000/health`
3. Firewall pode estar bloqueando porta 8000

### Problema: "HWID não corresponde"

**Solução:**
1. Usar botão "Liberar Licença" na GUI (Branch futura)
2. Chamar endpoint `/api/auth/release` manualmente
3. Reiniciar aplicação

### Problema: "Token expirado"

**Solução:**
1. Fazer novo login
2. Token tem validade de 7 dias

### Problema: Módulo não encontrado

**Solução:**
```bash
pip install -r requirements.txt
```

---

## 📝 Notas de Desenvolvimento

### Arquivos Modificados
- `gui_main.py`: Integração com autenticação
- `requirements.txt`: Novas dependências

### Arquivos Criados
- `src/hwid_generator.py`
- `src/auth_client.py`
- `src/login_window.py`
- `auth_server_mock.py`
- `BRANCH_04_SECURITY.md`

### Compatibilidade
- ✅ Windows (testado)
- ⚠️ Linux (precisa testar HWID)
- ⚠️ macOS (precisa testar HWID)

---

## 📚 Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Kiwify Webhooks](https://docs.kiwify.com.br/)

---

**Branch 04 concluída com sucesso! 🎉**

Próxima branch: Branch 05 - Face Tracking (Opcional)
