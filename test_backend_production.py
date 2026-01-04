"""
Script de Teste - Backend Production
Branch 04: Sistema de Segurança e Licenciamento

Testa estrutura do backend sem conectar ao banco real
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 Testando estrutura do Backend de Produção\n")
print("=" * 50)

# 1. Testar imports
print("\n1️⃣ Testando imports dos módulos...")
try:
    from backend.models import User, UserStatus
    print("   ✅ backend.models")
except Exception as e:
    print(f"   ❌ backend.models: {e}")

try:
    from backend.auth import hash_password, verify_password, create_access_token
    print("   ✅ backend.auth")
except Exception as e:
    print(f"   ❌ backend.auth: {e}")

try:
    from backend.database import Base, SessionLocal
    print("   ✅ backend.database")
except Exception as e:
    print(f"   ❌ backend.database: {e}")

# 2. Testar funções de autenticação
print("\n2️⃣ Testando funções de autenticação...")
try:
    # Hash de senha
    password = "test123"
    hashed = hash_password(password)
    print(f"   ✅ Hash gerado: {hashed[:32]}...")
    
    # Verificar senha
    if verify_password(password, hashed):
        print("   ✅ Verificação de senha")
    else:
        print("   ❌ Verificação de senha falhou")
    
    # Criar token JWT
    token = create_access_token({"sub": "test@example.com", "id": 1})
    print(f"   ✅ JWT Token gerado: {token[:32]}...")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Testar enum UserStatus
print("\n3️⃣ Testando enum UserStatus...")
try:
    statuses = [status.value for status in UserStatus]
    print(f"   ✅ Status disponíveis: {', '.join(statuses)}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 4. Testar modelo User (sem banco)
print("\n4️⃣ Testando modelo User (estrutura)...")
try:
    from backend.models import User
    
    # Verificar campos
    required_fields = ['id', 'email', 'password_hash', 'hardware_id', 'status', 
                       'expiration_date', 'created_at', 'kiwify_order_id']
    
    model_columns = [col.name for col in User.__table__.columns]
    
    for field in required_fields:
        if field in model_columns:
            print(f"   ✅ Campo {field}")
        else:
            print(f"   ❌ Campo {field} não encontrado")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 5. Verificar dependências
print("\n5️⃣ Verificando dependências instaladas...")
dependencies = [
    ("fastapi", "FastAPI"),
    ("sqlalchemy", "SQLAlchemy"),
    ("psycopg2", "PostgreSQL Driver"),
    ("pydantic", "Pydantic"),
    ("jwt", "PyJWT"),
    ("requests", "Requests"),
]

for module, name in dependencies:
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} não instalado")

# 6. Verificar arquivos de configuração
print("\n6️⃣ Verificando arquivos de configuração...")
files = [
    ("backend/api.py", "API Server"),
    ("backend/models.py", "Database Models"),
    ("backend/auth.py", "Auth Logic"),
    ("backend/database.py", "Database Config"),
    ("backend/init_db.py", "DB Init Script"),
    ("render.yaml", "Render Config"),
    (".env.example", "Env Template"),
]

for file_path, description in files:
    full_path = Path(__file__).parent / file_path
    if full_path.exists():
        print(f"   ✅ {description}: {file_path}")
    else:
        print(f"   ❌ {description}: {file_path} não encontrado")

print("\n" + "=" * 50)
print("\n✅ Teste concluído!")
print("\n📋 Próximos passos:")
print("   1. Instalar dependências: pip install -r requirements.txt")
print("   2. Configurar .env com DATABASE_URL do Neon.tech")
print("   3. Inicializar banco: python backend/init_db.py")
print("   4. Testar API localmente: python backend/api.py")
print("   5. Deploy no Render: seguir DEPLOY_GUIDE.md")
