"""
Módulo de Download de Vídeos
Utiliza yt-dlp para baixar vídeos do YouTube e extrair áudio
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import yt_dlp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoDownloader:
    """
    Gerencia o download de vídeos do YouTube e extração de áudio
    """
    
    def __init__(self, output_dir: str = "downloads"):
        """
        Args:
            output_dir: Diretório onde os arquivos serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_video(self, url: str, video_only: bool = False) -> Optional[str]:
        """
        Baixa o vídeo completo do YouTube
        
        Args:
            url: URL do vídeo do YouTube
            video_only: Se True, baixa apenas vídeo sem áudio (para economizar espaço)
            
        Returns:
            Caminho do arquivo de vídeo baixado ou None em caso de erro
        """
        try:
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
            
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if not video_only else 'bestvideo[ext=mp4]',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'merge_output_format': 'mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Baixando vídeo: {url}")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                logger.info(f"Vídeo baixado: {filename}")
                return filename
                
        except Exception as e:
            logger.error(f"Erro ao baixar vídeo: {e}")
            return None
    
    def download_audio(self, url: str, format: str = "wav") -> Optional[str]:
        """
        Baixa apenas o áudio do vídeo (mais rápido e econômico para transcrição)
        
        Args:
            url: URL do vídeo do YouTube
            format: Formato do áudio (wav, mp3, m4a)
            
        Returns:
            Caminho do arquivo de áudio baixado ou None em caso de erro
        """
        try:
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format,
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Baixando áudio: {url}")
                info = ydl.extract_info(url, download=True)
                
                # O nome do arquivo muda após a conversão
                base_filename = ydl.prepare_filename(info)
                audio_filename = os.path.splitext(base_filename)[0] + f".{format}"
                
                logger.info(f"Áudio baixado: {audio_filename}")
                return audio_filename
                
        except Exception as e:
            logger.error(f"Erro ao baixar áudio: {e}")
            return None
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        Obtém informações do vídeo sem fazer download
        
        Args:
            url: URL do vídeo do YouTube
            
        Returns:
            Dicionário com metadados do vídeo
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),  # segundos
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'description': info.get('description'),
                }
                
        except Exception as e:
            logger.error(f"Erro ao obter informações do vídeo: {e}")
            return None


# Teste do módulo
if __name__ == "__main__":
    downloader = VideoDownloader(output_dir="temp_downloads")
    
    # Exemplo de uso
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    # Obter informações
    info = downloader.get_video_info(test_url)
    if info:
        print(f"Título: {info['title']}")
        print(f"Duração: {info['duration']}s")
    
    # Baixar apenas áudio (recomendado para transcrição)
    # audio_file = downloader.download_audio(test_url)
