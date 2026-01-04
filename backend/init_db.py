"""
Database Initialization Script
Branch 04: Sistema de Segurança e Licenciamento

Script para inicializar banco de dados e criar usuário admin
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import init_db, SessionLocal
from backend.models import User, UserStatus
from backend.auth import hash_password
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user():
    """Cria usuário admin padrão se não existir"""
    db = SessionLocal()
    
    try:
        # Verificar se admin já existe
        admin = db.query(User).filter(User.email == "admin@clipperbot.com").first()
        
        if admin:
            logger.info("✅ Usuário admin já existe")
            return
        
        # Criar admin
        admin = User(
            email="admin@clipperbot.com",
            password_hash=hash_password("admin123"),  # Alterar após primeiro login!
            status=UserStatus.ACTIVE,
            expiration_date=datetime.now() + timedelta(days=365),  # 1 ano
            hardware_id=None
        )
        
        db.add(admin)
        db.commit()
        
        logger.info("✅ Usuário admin criado com sucesso")
        logger.info("   Email: admin@clipperbot.com")
        logger.info("   Senha: admin123")
        logger.info("   ⚠️  ALTERE A SENHA APÓS PRIMEIRO LOGIN!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar admin: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Inicializa banco de dados"""
    logger.info("🚀 Inicializando banco de dados...")
    
    try:
        # Criar tabelas
        init_db()
        logger.info("✅ Tabelas criadas com sucesso")
        
        # Criar usuário admin
        create_admin_user()
        
        logger.info("✅ Banco de dados inicializado!")
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
