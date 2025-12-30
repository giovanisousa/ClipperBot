#!/usr/bin/env python3
"""
AutoClipper Bot - Interface de Linha de Comando (CLI)
Branch 01: Prova de Conceito (POC) do Core Engine

Este script permite testar o fluxo completo de processamento:
1. Download de vídeo/áudio do YouTube
2. Transcrição usando Faster-Whisper
3. Análise de clímax (semântica + acústica)
4. Corte automatizado dos melhores momentos
"""

import argparse
import logging
import sys
from pathlib import Path

from src.downloader import VideoDownloader
from src.transcriber import AudioTranscriber
from src.analyzer import ClimaxAnalyzer
from src.video_cutter import VideoCutter

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('autoclipper.log')
    ]
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='AutoClipper Bot - Cortes inteligentes de vídeos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Processar vídeo do YouTube com palavras-chave padrão
  python main_cli.py --url "https://youtube.com/watch?v=..."

  # Definir palavras-chave personalizadas
  python main_cli.py --url "https://youtube.com/watch?v=..." --keywords "milhão,segredo,atenção"

  # Processar arquivo de vídeo local
  python main_cli.py --file "meu_video.mp4" --keywords "importante,incrível"

  # Ajustar sensibilidade de volume
  python main_cli.py --url "..." --min-volume -15 --keywords "wow,incrível"
        """
    )
    
    # Argumentos de entrada
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', type=str, help='URL do vídeo do YouTube')
    input_group.add_argument('--file', type=str, help='Caminho do arquivo de vídeo local')
    
    # Configurações de análise
    parser.add_argument(
        '--keywords',
        type=str,
        default='milhão,segredo,atenção,incrível,importante',
        help='Palavras-chave para identificar clímax (separadas por vírgula)'
    )
    parser.add_argument(
        '--ignore',
        type=str,
        default='patrocinador,inscreva-se,anúncio',
        help='Palavras para ignorar (separadas por vírgula)'
    )
    parser.add_argument(
        '--min-volume',
        type=float,
        default=-10.0,
        help='Volume mínimo em dB para considerar pico acústico (padrão: -10)'
    )
    parser.add_argument(
        '--min-duration',
        type=int,
        default=30,
        help='Duração mínima do corte em segundos (padrão: 30)'
    )
    parser.add_argument(
        '--max-duration',
        type=int,
        default=90,
        help='Duração máxima do corte em segundos (padrão: 90)'
    )
    
    # Configurações de modelo
    parser.add_argument(
        '--model',
        type=str,
        choices=['tiny', 'base', 'small', 'medium', 'large-v2'],
        default='small',
        help='Tamanho do modelo Whisper (padrão: small)'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='pt',
        help='Código do idioma para transcrição (padrão: pt)'
    )
    
    # Configurações de saída
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output_clips',
        help='Diretório para salvar os clipes (padrão: output_clips)'
    )
    parser.add_argument(
        '--max-clips',
        type=int,
        default=5,
        help='Número máximo de clipes para gerar (padrão: 5)'
    )
    
    # Opções avançadas
    parser.add_argument(
        '--skip-acoustic',
        action='store_true',
        help='Pular análise acústica (usar apenas palavras-chave)'
    )
    parser.add_argument(
        '--audio-only',
        action='store_true',
        help='Baixar apenas áudio (mais rápido para testes)'
    )
    
    args = parser.parse_args()
    
    # Banner
    print("=" * 60)
    print("🎬 AutoClipper Bot - Core Engine POC")
    print("=" * 60)
    print()
    
    try:
        # ETAPA 1: Download
        print("📥 ETAPA 1: Download")
        print("-" * 60)
        
        downloader = VideoDownloader(output_dir="downloads")
        
        if args.url:
            logger.info(f"Baixando do YouTube: {args.url}")
            
            # Obter informações do vídeo
            info = downloader.get_video_info(args.url)
            if info:
                print(f"📹 Título: {info['title']}")
                print(f"⏱️  Duração: {info['duration']}s ({info['duration']/60:.1f} min)")
                print()
            
            # Baixar vídeo e áudio
            video_path = downloader.download_video(args.url)
            audio_path = downloader.download_audio(args.url, format='wav')
            
            if not video_path or not audio_path:
                logger.error("Falha no download!")
                return 1
                
        else:
            video_path = args.file
            audio_path = args.file  # Usar o mesmo arquivo
            
            if not Path(video_path).exists():
                logger.error(f"Arquivo não encontrado: {video_path}")
                return 1
        
        print(f"✅ Download concluído!")
        print(f"   Vídeo: {video_path}")
        print(f"   Áudio: {audio_path}")
        print()
        
        # ETAPA 2: Transcrição
        print("🎤 ETAPA 2: Transcrição")
        print("-" * 60)
        
        transcriber = AudioTranscriber(model_size=args.model)
        transcription = transcriber.transcribe(
            audio_path,
            language=args.language,
            word_timestamps=True
        )
        
        if not transcription:
            logger.error("Falha na transcrição!")
            return 1
        
        print(f"✅ Transcrição concluída: {len(transcription)} segmentos")
        print(f"   Texto completo: {len(transcriber.get_full_text(transcription))} caracteres")
        print()
        
        # ETAPA 3: Análise de Clímax
        print("🔍 ETAPA 3: Análise de Clímax")
        print("-" * 60)
        
        keywords_climax = [k.strip() for k in args.keywords.split(',')]
        keywords_ignore = [k.strip() for k in args.ignore.split(',')]
        
        analyzer = ClimaxAnalyzer(
            keywords_climax=keywords_climax,
            keywords_ignore=keywords_ignore,
            min_volume_db=args.min_volume,
            cut_duration_min=args.min_duration,
            cut_duration_max=args.max_duration
        )
        
        # Análise semântica
        print(f"🔤 Buscando palavras-chave: {', '.join(keywords_climax)}")
        semantic_moments = analyzer.analyze_semantic(transcription)
        print(f"   Encontrados: {len(semantic_moments)} momentos semânticos")
        
        # Análise acústica
        acoustic_moments = []
        if not args.skip_acoustic:
            print(f"🔊 Analisando picos de volume (>{args.min_volume}dB)...")
            acoustic_moments = analyzer.analyze_acoustic(audio_path)
            print(f"   Encontrados: {len(acoustic_moments)} picos acústicos")
        
        # Combinar análises
        all_moments = analyzer.combine_analyses(semantic_moments, acoustic_moments)
        print(f"✅ Total de momentos identificados: {len(all_moments)}")
        
        # Criar pontos de corte
        cut_points = analyzer.create_cut_points(all_moments)
        
        # Limitar número de clipes
        if len(cut_points) > args.max_clips:
            print(f"⚠️  Limitando para os {args.max_clips} melhores momentos")
            cut_points = cut_points[:args.max_clips]
        
        print()
        print("📋 Pontos de Corte Identificados:")
        for i, cut in enumerate(cut_points, 1):
            print(f"   {i}. [{cut['start']:.1f}s - {cut['end']:.1f}s] "
                  f"({cut['duration']:.1f}s) - {cut['reason']}")
        print()
        
        # ETAPA 4: Corte de Vídeo
        print("✂️  ETAPA 4: Corte de Vídeo")
        print("-" * 60)
        
        cutter = VideoCutter(output_dir=args.output_dir)
        
        # Obter informações do vídeo
        video_info = cutter.get_video_info(video_path)
        if video_info:
            print(f"📹 Vídeo original: {video_info['width']}x{video_info['height']} "
                  f"@ {video_info['fps']:.1f}fps")
        
        # Cortar os segmentos
        output_files = cutter.cut_multiple_segments(
            input_video=video_path,
            cut_points=cut_points,
            prefix="autoclipper"
        )
        
        print(f"✅ Processamento concluído!")
        print(f"   Clipes gerados: {len(output_files)}")
        print()
        
        # Resumo final
        print("=" * 60)
        print("📊 RESUMO FINAL")
        print("=" * 60)
        print(f"Vídeo processado: {Path(video_path).name}")
        print(f"Clipes gerados: {len(output_files)}")
        print(f"Diretório de saída: {args.output_dir}")
        print()
        print("Arquivos gerados:")
        for i, file in enumerate(output_files, 1):
            size_mb = Path(file).stat().st_size / (1024 * 1024)
            print(f"  {i}. {Path(file).name} ({size_mb:.1f} MB)")
        print()
        print("🎉 Pronto para postar no TikTok/Reels!")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
