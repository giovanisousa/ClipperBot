"""
Mock Authentication API Server
Branch 04: Sistema de Segurança e Licenciamento

Servidor de autenticação MOCK para testes locais.
Na produção, substituir por servidor FastAPI completo com banco de dados.

ATENÇÃO: Este é apenas um mock para desenvolvimento!
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import secrets
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(title="ClipperBot Auth API (MOCK)", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# MOCK DATABASE (Em memória - apenas para testes)
# ========================================

# Usuários mock (senha: "demo123" com hash MD5)
MOCK_USERS = {
    "demo@clipperbot.com": {
        "id": 1,
        "email": "demo@clipperbot.com",
        "password_hash": hashlib.md5("demo123".encode()).hexdigest(),
        "hardware_id": None,  # Será preenchido no primeiro login
        "status": "active",
        "expiration_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "created_at": datetime.now().isoformat(),
        "last_reset": None
    },
    "test@example.com": {
        "id": 2,
        "email": "test@example.com",
        "password_hash": hashlib.md5("test123".encode()).hexdigest(),
        "hardware_id": None,
        "status": "active",
        "expiration_date": (datetime.now() + timedelta(days=15)).isoformat(),
        "created_at": datetime.now().isoformat(),
        "last_reset": None
    }
}

# Tokens ativos (em memória)
ACTIVE_TOKENS = {}


# ========================================
# MODELOS PYDANTIC
# ========================================

class LoginRequest(BaseModel):
    email: str
    password: str
    hwid: str


class ReleaseRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# ========================================
# ENDPOINTS
# ========================================

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "ClipperBot Auth API",
        "version": "1.0.0 (MOCK)",
        "status": "running",
        "warning": "Este é um servidor MOCK para desenvolvimento"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Endpoint de login
    
    Validações:
    1. Email e senha corretos
    2. Status da conta (active/inactive)
    3. Data de expiração
    4. Hardware ID (lock de 1 PC)
    """
    logger.info(f"🔐 Tentativa de login: {request.email}")
    
    # Buscar usuário
    user = MOCK_USERS.get(request.email)
    
    # 1. Validar credenciais
    if not user:
        logger.warning(f"❌ Usuário não encontrado: {request.email}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar senha (MD5 simples para mock)
    password_hash = hashlib.md5(request.password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        logger.warning(f"❌ Senha incorreta para: {request.email}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # 2. Verificar status da conta
    if user["status"] != "active":
        logger.warning(f"❌ Conta inativa: {request.email}")
        raise HTTPException(
            status_code=403,
            detail=f"Conta {user['status']}. Entre em contato com o suporte."
        )
    
    # 3. Verificar expiração
    expiration_date = datetime.fromisoformat(user["expiration_date"])
    if datetime.now() > expiration_date:
        logger.warning(f"❌ Assinatura expirada: {request.email}")
        raise HTTPException(
            status_code=403,
            detail="Sua assinatura expirou. Renove para continuar usando."
        )
    
    # 4. Verificar Hardware ID (1-PC-Lock)
    if user["hardware_id"] is None:
        # Primeiro login: registrar HWID
        user["hardware_id"] = request.hwid
        logger.info(f"✅ HWID registrado: {request.hwid[:16]}...")
    
    elif user["hardware_id"] != request.hwid:
        # Tentativa de usar em outro PC
        logger.warning(f"❌ HWID diferente: esperado={user['hardware_id'][:16]}..., recebido={request.hwid[:16]}...")
        raise HTTPException(
            status_code=409,
            detail="Esta licença já está em uso em outro computador"
        )
    
    # 5. Gerar token JWT (simplificado para mock)
    token = secrets.token_urlsafe(32)
    ACTIVE_TOKENS[token] = {
        "email": request.email,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=7)
    }
    
    # 6. Retornar sucesso
    logger.info(f"✅ Login bem-sucedido: {request.email}")
    
    return LoginResponse(
        access_token=token,
        user={
            "id": user["id"],
            "email": user["email"],
            "status": user["status"],
            "expiration_date": user["expiration_date"],
            "created_at": user["created_at"]
        }
    )


@app.get("/api/auth/validate")
async def validate(authorization: Optional[str] = Header(None)):
    """
    Valida token JWT
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    
    token = authorization.replace("Bearer ", "")
    
    token_data = ACTIVE_TOKENS.get(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Verificar expiração
    if datetime.now() > token_data["expires_at"]:
        del ACTIVE_TOKENS[token]
        raise HTTPException(status_code=401, detail="Token expirado")
    
    return {
        "valid": True,
        "email": token_data["email"],
        "expires_at": token_data["expires_at"].isoformat()
    }


@app.post("/api/auth/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    Faz logout e invalida token
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        if token in ACTIVE_TOKENS:
            del ACTIVE_TOKENS[token]
            return {"message": "Logout realizado com sucesso"}
    
    return {"message": "Nenhum token ativo"}


@app.post("/api/auth/release")
async def release_license(request: ReleaseRequest):
    """
    Libera licença do HWID atual
    Permite usar em outro PC
    """
    logger.info(f"🔓 Solicitação de liberação: {request.email}")
    
    # Buscar usuário
    user = MOCK_USERS.get(request.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar senha
    password_hash = hashlib.md5(request.password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Limpar HWID
    user["hardware_id"] = None
    logger.info(f"✅ Licença liberada: {request.email}")
    
    return {
        "message": "Licença liberada com sucesso",
        "email": request.email
    }


@app.post("/api/webhooks/kiwify")
async def kiwify_webhook(payload: dict):
    """
    Webhook do Kiwify
    
    Eventos tratados:
    - order.approved: Nova venda aprovada
    - subscription.cancelled: Assinatura cancelada
    - subscription.renewed: Assinatura renovada
    """
    logger.info(f"📥 Webhook Kiwify recebido: {payload.get('event_type')}")
    
    event_type = payload.get("event_type")
    customer_email = payload.get("customer", {}).get("email")
    
    if not event_type or not customer_email:
        raise HTTPException(status_code=400, detail="Payload inválido")
    
    # Processar evento
    if event_type == "order.approved":
        # Nova venda: criar/atualizar usuário
        logger.info(f"✅ Nova venda aprovada: {customer_email}")
        # TODO: Criar usuário no banco de dados
        
    elif event_type == "subscription.cancelled":
        # Cancelamento: desativar conta
        logger.info(f"❌ Assinatura cancelada: {customer_email}")
        # TODO: Marcar status como 'inactive'
        
    elif event_type == "subscription.renewed":
        # Renovação: estender data de expiração
        logger.info(f"🔄 Assinatura renovada: {customer_email}")
        # TODO: Atualizar expiration_date
    
    return {"message": "Webhook processado com sucesso"}


# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("🚀 ClipperBot Auth API (MOCK) - Iniciando...")
    print("=" * 50)
    print(f"\n📋 Usuários de teste:")
    for email, user in MOCK_USERS.items():
        print(f"  • {email}")
        print(f"    Senha: demo123 ou test123")
        print(f"    Status: {user['status']}")
        print(f"    Expira: {user['expiration_date'][:10]}\n")
    
    print("🌐 API disponível em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("=" * 50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
