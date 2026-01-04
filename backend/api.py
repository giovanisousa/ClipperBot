"""
FastAPI Production Server
Branch 04: Sistema de Segurança e Licenciamento

Servidor de autenticação para deploy no Render.com
Banco de dados: Neon.tech (PostgreSQL)
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from backend.database import get_db, init_db
from backend.models import User, UserStatus
from backend.auth import (
    verify_password,
    hash_password,
    create_access_token,
    verify_token,
    validate_credentials,
    reset_hardware_id,
    can_reset_hardware
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="ClipperBot Auth API",
    version="1.0.0",
    description="API de Autenticação e Licenciamento"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# MODELOS PYDANTIC
# ========================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    hwid: str


class ReleaseRequest(BaseModel):
    email: EmailStr
    password: str


class ResetRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class KiwifyWebhook(BaseModel):
    event_type: str
    order_id: Optional[str] = None
    subscription_id: Optional[str] = None
    customer: dict
    product: dict
    status: Optional[str] = None


# ========================================
# DEPENDENCY: Autenticação JWT
# ========================================

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency para extrair usuário do token JWT
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user


# ========================================
# STARTUP EVENT
# ========================================

@app.on_event("startup")
async def startup_event():
    """Inicializa banco de dados ao iniciar"""
    logger.info("🚀 Iniciando API de Autenticação...")
    logger.info("📊 Inicializando banco de dados...")
    init_db()
    logger.info("✅ Banco de dados inicializado")


# ========================================
# ENDPOINTS
# ========================================

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "ClipperBot Auth API",
        "version": "1.0.0",
        "status": "running",
        "database": "Neon.tech PostgreSQL"
    }


@app.get("/health")
async def health(db: Session = Depends(get_db)):
    """Health check com verificação de banco"""
    try:
        # Testar conexão com banco
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login
    
    Validações:
    1. Email e senha corretos
    2. Status da conta (active)
    3. Data de expiração
    4. Hardware ID (1-PC-Lock)
    """
    logger.info(f"🔐 Tentativa de login: {request.email}")
    
    # Validar credenciais
    success, user, error = validate_credentials(
        db, request.email, request.password, request.hwid
    )
    
    if not success:
        if error == "hardware_mismatch":
            logger.warning(f"❌ HWID não corresponde: {request.email}")
            raise HTTPException(
                status_code=409,
                detail="Esta licença já está em uso em outro computador"
            )
        else:
            logger.warning(f"❌ Falha no login: {request.email} - {error}")
            
            if "expirou" in error.lower():
                raise HTTPException(status_code=403, detail=error)
            else:
                raise HTTPException(status_code=401, detail=error)
    
    # Gerar token JWT
    token = create_access_token({"sub": user.email, "id": user.id})
    
    logger.info(f"✅ Login bem-sucedido: {request.email}")
    
    return LoginResponse(
        access_token=token,
        user=user.to_dict()
    )


@app.get("/api/auth/validate")
async def validate(current_user: User = Depends(get_current_user)):
    """
    Valida token JWT e retorna dados do usuário
    """
    return {
        "valid": True,
        "user": current_user.to_dict()
    }


@app.post("/api/auth/logout")
async def logout():
    """
    Logout (JWT é stateless, então apenas confirmação)
    """
    return {"message": "Logout realizado com sucesso"}


@app.post("/api/auth/release")
async def release_license(request: ReleaseRequest, db: Session = Depends(get_db)):
    """
    Libera licença do HWID atual
    Permite usar em outro PC imediatamente
    """
    logger.info(f"🔓 Solicitação de liberação: {request.email}")
    
    # Buscar usuário
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar senha
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Limpar HWID
    user.hardware_id = None
    db.commit()
    
    logger.info(f"✅ Licença liberada: {request.email}")
    
    return {
        "message": "Licença liberada com sucesso",
        "email": request.email
    }


@app.post("/api/auth/reset")
async def reset_hardware(request: ResetRequest, db: Session = Depends(get_db)):
    """
    Reset mensal do Hardware ID
    Permite trocar de PC 1x por mês
    """
    logger.info(f"🔄 Solicitação de reset: {request.email}")
    
    # Buscar usuário
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar senha
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar se pode resetar
    can_reset, error = can_reset_hardware(user)
    
    if not can_reset:
        raise HTTPException(status_code=429, detail=error)
    
    # Resetar
    if reset_hardware_id(db, user):
        logger.info(f"✅ Hardware ID resetado: {request.email}")
        return {
            "message": "Hardware ID resetado com sucesso",
            "email": request.email
        }
    else:
        raise HTTPException(status_code=500, detail="Erro ao resetar hardware ID")


@app.post("/api/webhooks/kiwify")
async def kiwify_webhook(payload: KiwifyWebhook, db: Session = Depends(get_db)):
    """
    Webhook do Kiwify para gerenciar licenças
    
    Eventos:
    - order.approved: Nova venda
    - subscription.cancelled: Cancelamento
    - subscription.renewed: Renovação
    """
    logger.info(f"📥 Webhook Kiwify: {payload.event_type}")
    
    customer_email = payload.customer.get("email")
    
    if not customer_email:
        raise HTTPException(status_code=400, detail="Email do cliente ausente")
    
    # Processar evento
    if payload.event_type == "order.approved":
        # Nova venda: criar ou reativar usuário
        user = db.query(User).filter(User.email == customer_email).first()
        
        if not user:
            # Criar novo usuário
            # Senha temporária: primeiros 8 caracteres do order_id
            temp_password = payload.order_id[:8] if payload.order_id else "clipper123"
            
            user = User(
                email=customer_email,
                password_hash=hash_password(temp_password),
                status=UserStatus.ACTIVE,
                expiration_date=datetime.now() + timedelta(days=30),  # 30 dias
                kiwify_order_id=payload.order_id,
                kiwify_subscription_id=payload.subscription_id
            )
            db.add(user)
            logger.info(f"✅ Novo usuário criado: {customer_email}")
        else:
            # Reativar usuário existente
            user.status = UserStatus.ACTIVE
            user.expiration_date = datetime.now() + timedelta(days=30)
            user.kiwify_order_id = payload.order_id
            logger.info(f"✅ Usuário reativado: {customer_email}")
        
        db.commit()
        
    elif payload.event_type == "subscription.cancelled":
        # Cancelamento: desativar conta
        user = db.query(User).filter(User.email == customer_email).first()
        
        if user:
            user.status = UserStatus.INACTIVE
            db.commit()
            logger.info(f"❌ Usuário desativado: {customer_email}")
        
    elif payload.event_type == "subscription.renewed":
        # Renovação: estender expiração
        user = db.query(User).filter(User.email == customer_email).first()
        
        if user:
            user.status = UserStatus.ACTIVE
            user.expiration_date = datetime.now() + timedelta(days=30)
            db.commit()
            logger.info(f"🔄 Assinatura renovada: {customer_email}")
    
    return {"message": "Webhook processado com sucesso"}


# ========================================
# ADMIN ENDPOINTS (Protegidos)
# ========================================

@app.get("/api/admin/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os usuários (apenas admin)
    """
    # TODO: Implementar verificação de admin
    users = db.query(User).all()
    return {
        "users": [user.to_dict() for user in users],
        "total": len(users)
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("🚀 ClipperBot Auth API - Produção")
    print("=" * 50)
    print("🌐 API disponível em: http://0.0.0.0:8000")
    print("📚 Documentação: http://0.0.0.0:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
