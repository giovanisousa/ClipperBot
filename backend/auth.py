"""
Authentication Logic
Branch 04: Sistema de Segurança e Licenciamento

Lógica de autenticação, JWT tokens e validação de hardware
"""

import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
from sqlalchemy.orm import Session

from backend.models import User, UserStatus


# Configurações JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    """
    Gera hash da senha usando SHA256
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash SHA256 da senha
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se senha corresponde ao hash
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash armazenado
        
    Returns:
        True se corresponde, False caso contrário
    """
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict) -> str:
    """
    Cria JWT access token
    
    Args:
        data: Dados a serem codificados no token
        
    Returns:
        JWT token codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica e decodifica JWT token
    
    Args:
        token: JWT token
        
    Returns:
        Payload decodificado ou None se inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def validate_credentials(
    db: Session,
    email: str,
    password: str,
    hwid: str
) -> Tuple[bool, Optional[User], Optional[str]]:
    """
    Valida credenciais e hardware ID
    
    Validações:
    1. Email e senha corretos
    2. Status da conta (active)
    3. Data de expiração
    4. Hardware ID (1-PC-Lock)
    
    Args:
        db: Sessão do banco
        email: Email do usuário
        password: Senha
        hwid: Hardware ID da máquina
        
    Returns:
        Tupla (sucesso, usuário, mensagem_erro)
    """
    # 1. Buscar usuário
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return False, None, "Credenciais inválidas"
    
    # 2. Verificar senha
    if not verify_password(password, user.password_hash):
        return False, None, "Credenciais inválidas"
    
    # 3. Verificar status
    if user.status != UserStatus.ACTIVE:
        if user.status == UserStatus.EXPIRED:
            return False, None, "Sua assinatura expirou. Renove para continuar."
        elif user.status == UserStatus.SUSPENDED:
            return False, None, "Conta suspensa. Entre em contato com o suporte."
        else:
            return False, None, f"Conta {user.status.value}. Entre em contato com o suporte."
    
    # 4. Verificar expiração
    if user.expiration_date and datetime.now() > user.expiration_date.replace(tzinfo=None):
        user.status = UserStatus.EXPIRED
        db.commit()
        return False, None, "Sua assinatura expirou. Renove para continuar."
    
    # 5. Verificar Hardware ID (1-PC-Lock)
    if user.hardware_id is None:
        # Primeiro login: registrar HWID
        user.hardware_id = hwid
        user.last_login = datetime.now()
        db.commit()
        return True, user, None
    
    elif user.hardware_id != hwid:
        # Tentativa de usar em outro PC
        return False, None, "hardware_mismatch"
    
    # 6. Sucesso: atualizar último login
    user.last_login = datetime.now()
    db.commit()
    
    return True, user, None


def can_reset_hardware(user: User) -> Tuple[bool, Optional[str]]:
    """
    Verifica se usuário pode resetar hardware ID
    Regra: 1 reset por mês
    
    Args:
        user: Objeto User
        
    Returns:
        Tupla (pode_resetar, mensagem_erro)
    """
    if user.last_reset is None:
        return True, None
    
    # Verificar se passou 30 dias
    days_since_reset = (datetime.now() - user.last_reset.replace(tzinfo=None)).days
    
    if days_since_reset >= 30:
        return True, None
    else:
        days_remaining = 30 - days_since_reset
        return False, f"Você poderá resetar novamente em {days_remaining} dias"


def reset_hardware_id(db: Session, user: User) -> bool:
    """
    Reseta hardware ID do usuário
    
    Args:
        db: Sessão do banco
        user: Objeto User
        
    Returns:
        True se resetado com sucesso
    """
    can_reset, error = can_reset_hardware(user)
    
    if not can_reset:
        return False
    
    user.hardware_id = None
    user.last_reset = datetime.now()
    user.reset_count += 1
    db.commit()
    
    return True
