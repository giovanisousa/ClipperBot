"""
Database Configuration
Branch 04: Sistema de Segurança e Licenciamento

Configuração do banco de dados PostgreSQL (Neon.tech)
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL do banco de dados (Neon.tech PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@host/database"  # Placeholder
)

# Configuração do engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexão antes de usar
    pool_size=10,  # Conexões no pool
    max_overflow=20,  # Conexões extras quando pool cheio
    echo=False  # True para debug SQL
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco
    
    Yields:
        Session do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados
    Cria todas as tabelas
    """
    from backend.models import User  # Import aqui para evitar circular
    Base.metadata.create_all(bind=engine)
