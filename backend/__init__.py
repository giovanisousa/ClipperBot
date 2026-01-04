"""
Backend Module
Branch 04: Sistema de Segurança e Licenciamento
"""

from backend.database import get_db, init_db
from backend.models import User, UserStatus
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

__all__ = [
    "get_db",
    "init_db",
    "User",
    "UserStatus",
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_token"
]
