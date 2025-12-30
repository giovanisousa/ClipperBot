"""
Testes Básicos dos Módulos - Branch 01
Execute este arquivo para validar que todos os módulos estão funcionando
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Testa se todas as dependências foram instaladas corretamente"""
    print("🧪 Testando importações...")
    
    try:
        import yt_dlp
        print("✅ yt-dlp")
    except ImportError:
        print("❌ yt-dlp não instalado")
        return False
    
    try:
        from faster_whisper import WhisperModel
        print("✅ faster-whisper")
    except ImportError:
        print("❌ faster-whisper não instalado")
        return False
    
    try:
        import ffmpeg
        print("✅ ffmpeg-python")
    except ImportError:
        print("❌ ffmpeg-python não instalado")
        return False
    
    try:
        import librosa
        print("✅ librosa")
    except ImportError:
        print("❌ librosa não instalado")
        return False
    
    try:
        from pydub import AudioSegment
        print("✅ pydub")
    except ImportError:
        print("❌ pydub não instalado")
        return False
    
    try:
        import numpy
        print("✅ numpy")
    except ImportError:
        print("❌ numpy não instalado")
        return False
    
    return True


def test_ffmpeg_binary():
    """Testa se o FFmpeg binário está disponível no sistema"""
    print("\n🧪 Testando FFmpeg binário...")
    
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        version_line = result.stdout.decode().split('\n')[0]
        print(f"✅ FFmpeg encontrado: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg não encontrado no sistema")
        print("   Instale com: sudo apt install ffmpeg (Linux)")
        return False


def test_modules():
    """Testa se os módulos do projeto podem ser importados"""
    print("\n🧪 Testando módulos do projeto...")
    
    try:
        from src.downloader import VideoDownloader
        print("✅ src.downloader")
    except ImportError as e:
        print(f"❌ src.downloader: {e}")
        return False
    
    try:
        from src.transcriber import AudioTranscriber
        print("✅ src.transcriber")
    except ImportError as e:
        print(f"❌ src.transcriber: {e}")
        return False
    
    try:
        from src.analyzer import ClimaxAnalyzer
        print("✅ src.analyzer")
    except ImportError as e:
        print(f"❌ src.analyzer: {e}")
        return False
    
    try:
        from src.video_cutter import VideoCutter
        print("✅ src.video_cutter")
    except ImportError as e:
        print(f"❌ src.video_cutter: {e}")
        return False
    
    return True


def test_whisper_model():
    """Testa se o modelo Whisper pode ser carregado"""
    print("\n🧪 Testando modelo Whisper (pode demorar na primeira vez)...")
    
    try:
        from faster_whisper import WhisperModel
        
        print("   Carregando modelo 'tiny' (teste rápido)...")
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        print("✅ Modelo Whisper carregado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return False


def main():
    print("=" * 60)
    print("🔧 AutoClipper Bot - Teste de Ambiente")
    print("=" * 60)
    print()
    
    all_tests_passed = True
    
    # Teste 1: Importações
    if not test_imports():
        all_tests_passed = False
        print("\n⚠️  Algumas dependências não estão instaladas.")
        print("   Execute: pip install -r requirements.txt")
    
    # Teste 2: FFmpeg
    if not test_ffmpeg_binary():
        all_tests_passed = False
    
    # Teste 3: Módulos do projeto
    if not test_modules():
        all_tests_passed = False
    
    # Teste 4: Modelo Whisper (opcional)
    print("\n❓ Deseja testar o carregamento do modelo Whisper?")
    print("   (Isso vai baixar ~75MB na primeira vez)")
    response = input("   Digite 's' para sim, qualquer tecla para pular: ")
    
    if response.lower() == 's':
        if not test_whisper_model():
            all_tests_passed = False
    else:
        print("⏭️  Pulando teste do modelo Whisper")
    
    # Resumo
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n🎉 Ambiente configurado corretamente!")
        print("\nPróximos passos:")
        print("  1. Leia INSTALL.md para instruções de uso")
        print("  2. Execute: python main_cli.py --help")
        print("  3. Teste com um vídeo curto do YouTube")
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("=" * 60)
        print("\n⚠️  Configure o ambiente antes de continuar")
        print("\nVeja INSTALL.md para instruções detalhadas")
        return 1


if __name__ == "__main__":
    sys.exit(main())
