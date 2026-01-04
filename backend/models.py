"""
Database Models
Branch 04: Sistema de Segurança e Licenciamento

Modelos SQLAlchemy para PostgreSQL (Neon.tech)
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from backend.database import Base


class UserStatus(enum.Enum):
    """Status da conta do usuário"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class User(Base):
    """
    Modelo de usuário
    
    Tabela principal de autenticação e licenciamento
    """
    __tablename__ = "users"
    
    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Hardware Lock (1-PC-per-License)
    hardware_id = Column(String(64), nullable=True, index=True)
    
    # Status e Expiração
    status = Column(
        SQLEnum(UserStatus),
        default=UserStatus.ACTIVE,
        nullable=False
    )
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    
    # Gerenciamento de Reset
    last_reset = Column(DateTime(timezone=True), nullable=True)
    reset_count = Column(Integer, default=0)
    
    # Integração Kiwify
    kiwify_order_id = Column(String(255), nullable=True, index=True)
    kiwify_subscription_id = Column(String(255), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', status='{self.status.value}')>"
    
    def to_dict(self):
        """Serializa para dicionário (sem senha)"""
        return {
            "id": self.id,
            "email": self.email,
            "status": self.status.value,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
