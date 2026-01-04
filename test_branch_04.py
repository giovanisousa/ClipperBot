"""
Quick Test Script - Branch 04
Testa todos os componentes de segurança rapidamente
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

print("=" * 60)
print("🔐 TESTE RÁPIDO - Branch 04: Segurança e Licenciamento")
print("=" * 60)
print()

# ========================================
# Teste 1: Hardware ID Generator
# ========================================
print("📝 Teste 1: Hardware ID Generator")
print("-" * 60)

try:
    from src.hwid_generator import HardwareIDGenerator
    
    hwid1 = HardwareIDGenerator.generate_hwid()
    hwid2 = HardwareIDGenerator.generate_hwid()
    
    print(f"✅ HWID gerado: {hwid1}")
    print(f"✅ Tamanho: {len(hwid1)} caracteres")
    print(f"✅ Consistente: {hwid1 == hwid2}")
    
    # Verificação
    is_valid = HardwareIDGenerator.verify_hwid(hwid1)
    print(f"✅ Verificação: {'PASSOU' if is_valid else 'FALHOU'}")
    
    print()
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    print()


# ========================================
# Teste 2: Auth Client (sem servidor)
# ========================================
print("📝 Teste 2: Auth Client (Verificação de Estrutura)")
print("-" * 60)

try:
    from src.auth_client import AuthClient
    
    client = AuthClient()
    print(f"✅ API Base URL: {client.API_BASE_URL}")
    print(f"✅ Token File: {client.TOKEN_FILE}")
    print(f"✅ Autenticado: {client.is_authenticated()}")
    
    print()
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    print()


# ========================================
# Teste 3: Verificar Dependências
# ========================================
print("📝 Teste 3: Verificar Dependências")
print("-" * 60)

dependencies = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("pydantic", "Pydantic"),
    ("requests", "Requests"),
    ("customtkinter", "CustomTkinter")
]

all_ok = True
for module_name, display_name in dependencies:
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
    except ImportError:
        print(f"❌ {display_name} - NÃO INSTALADO")
        all_ok = False

print()

if not all_ok:
    print("⚠️  Instalar dependências faltantes:")
    print("   pip install -r requirements.txt")
    print()


# ========================================
# Teste 4: Verificar Mock Server
# ========================================
print("📝 Teste 4: Verificar Mock Server (Opcional)")
print("-" * 60)

try:
    import requests
    
    response = requests.get("http://localhost:8000/health", timeout=2)
    
    if response.status_code == 200:
        print("✅ Mock Server está RODANDO")
        print(f"   Status: {response.json().get('status')}")
    else:
        print(f"⚠️  Mock Server respondeu com código: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("⚠️  Mock Server NÃO está rodando")
    print("   Iniciar com: python auth_server_mock.py")
    
except Exception as e:
    print(f"❌ Erro ao verificar servidor: {e}")

print()


# ========================================
# Teste 5: Estrutura de Arquivos
# ========================================
print("📝 Teste 5: Estrutura de Arquivos")
print("-" * 60)

required_files = [
    "src/hwid_generator.py",
    "src/auth_client.py",
    "src/login_window.py",
    "auth_server_mock.py",
    "gui_main.py",
    "requirements.txt"
]

for file_path in required_files:
    path = Path(file_path)
    if path.exists():
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - NÃO ENCONTRADO")

print()


# ========================================
# Resumo
# ========================================
print("=" * 60)
print("📊 RESUMO")
print("=" * 60)
print()
print("Para testar o sistema completo:")
print()
print("1️⃣  Iniciar servidor mock:")
print("   python auth_server_mock.py")
print()
print("2️⃣  Em outro terminal, executar GUI:")
print("   python gui_main.py")
print()
print("3️⃣  Credenciais de teste:")
print("   Email: demo@clipperbot.com")
print("   Senha: demo123")
print()
print("=" * 60)
