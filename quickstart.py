#!/usr/bin/env python3
"""
Quick Start - AutoClipper Bot
Script interativo para primeiros passos
"""

import sys
import subprocess
from pathlib import Path


def print_banner():
    print("=" * 70)
    print("🎬 AutoClipper Bot - Quick Start")
    print("=" * 70)
    print()


def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_venv():
    """Verifica se está em ambiente virtual"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Ambiente virtual ativo")
    else:
        print("⚠️  Ambiente virtual não detectado")
        print("   Recomendado: python -m venv venv && source venv/bin/activate")
    
    return in_venv


def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    deps = [
        'yt_dlp',
        'faster_whisper',
        'ffmpeg',
        'librosa',
        'pydub'
    ]
    
    missing = []
    
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    return len(missing) == 0, missing


def check_ffmpeg():
    """Verifica se FFmpeg está instalado"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print("✅ FFmpeg instalado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg não encontrado")
        print("   Instale com: sudo apt install ffmpeg")
        return False


def suggest_actions(missing_deps, has_ffmpeg):
    """Sugere próximas ações"""
    print("\n" + "=" * 70)
    print("📋 PRÓXIMAS AÇÕES")
    print("=" * 70)
    
    if missing_deps:
        print("\n1️⃣ Instalar dependências Python:")
        print("   pip install -r requirements.txt")
    
    if not has_ffmpeg:
        print("\n2️⃣ Instalar FFmpeg:")
        print("   sudo apt install ffmpeg  # Linux")
    
    if not missing_deps and has_ffmpeg:
        print("\n✅ Tudo pronto! Você pode:")
        print("\n1️⃣ Ver ajuda:")
        print("   python main_cli.py --help")
        
        print("\n2️⃣ Testar com um vídeo:")
        print('   python main_cli.py --url "https://youtube.com/watch?v=..."')
        
        print("\n3️⃣ Ver exemplos:")
        print("   cat examples/README.md")
        
        print("\n4️⃣ Ler documentação completa:")
        print("   cat INSTALL.md")


def interactive_test():
    """Teste interativo opcional"""
    print("\n" + "=" * 70)
    print("🧪 TESTE INTERATIVO")
    print("=" * 70)
    
    response = input("\nDeseja fazer um teste rápido? (s/N): ")
    
    if response.lower() == 's':
        print("\n📥 Teste de download de metadados...")
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        try:
            from src.downloader import VideoDownloader
            downloader = VideoDownloader(output_dir="test_temp")
            info = downloader.get_video_info(test_url)
            
            if info:
                print("✅ Download de metadados funcionando!")
                print(f"   Título: {info['title']}")
                print(f"   Duração: {info['duration']}s")
            else:
                print("❌ Falha ao obter metadados")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n🎤 Teste de modelo Whisper...")
    response = input("Deseja carregar o modelo Whisper? (pode demorar) (s/N): ")
    
    if response.lower() == 's':
        try:
            from faster_whisper import WhisperModel
            print("   Carregando modelo 'tiny' (teste rápido)...")
            model = WhisperModel("tiny", device="cpu", compute_type="int8")
            print("✅ Modelo Whisper carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")


def main():
    print_banner()
    
    print("🔍 Verificando ambiente...\n")
    
    # Verificações
    has_python = check_python_version()
    has_venv = check_venv()
    has_deps, missing_deps = check_dependencies()
    has_ffmpeg = check_ffmpeg()
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    
    all_good = has_python and has_deps and has_ffmpeg
    
    if all_good:
        print("\n✅ AMBIENTE CONFIGURADO CORRETAMENTE!")
        print("   Você está pronto para usar o AutoClipper Bot!")
    else:
        print("\n⚠️  CONFIGURAÇÃO INCOMPLETA")
        print("   Siga as instruções abaixo para completar a instalação.")
    
    # Sugestões
    suggest_actions(missing_deps, has_ffmpeg)
    
    # Teste interativo (só se tudo estiver ok)
    if all_good:
        try:
            interactive_test()
        except KeyboardInterrupt:
            print("\n\n⚠️  Teste cancelado")
    
    print("\n" + "=" * 70)
    print("📚 Para mais informações:")
    print("   • INSTALL.md - Guia de instalação completo")
    print("   • README.md - Visão geral do projeto")
    print("   • examples/README.md - Exemplos de uso")
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
        sys.exit(0)
