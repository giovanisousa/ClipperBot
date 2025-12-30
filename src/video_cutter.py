"""
Módulo de Corte de Vídeo
Utiliza FFmpeg para extrair segmentos de vídeo baseado em timestamps
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
import ffmpeg
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoCutter:
    """
    Gerencia o corte e processamento de vídeos usando FFmpeg
    """
    
    def __init__(self, output_dir: str = "clips"):
        """
        Args:
            output_dir: Diretório onde os clipes serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar se FFmpeg está disponível
        if not self._check_ffmpeg():
            raise RuntimeError(
                "FFmpeg não encontrado! Instale com: sudo apt install ffmpeg (Linux) "
                "ou baixe de https://ffmpeg.org/download.html"
            )
    
    def _check_ffmpeg(self) -> bool:
        """Verifica se FFmpeg está instalado"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def cut_video(
        self,
        input_video: str,
        start_time: float,
        end_time: float,
        output_filename: str = None,
        reencode: bool = False
    ) -> Optional[str]:
        """
        Corta um segmento do vídeo
        
        Args:
            input_video: Caminho do vídeo original
            start_time: Tempo de início do corte (segundos)
            end_time: Tempo de fim do corte (segundos)
            output_filename: Nome do arquivo de saída (gerado automaticamente se None)
            reencode: Se True, re-codifica o vídeo (mais lento, mais preciso)
                     Se False, faz stream copy (rápido, pode ter imprecisão)
            
        Returns:
            Caminho do arquivo de vídeo cortado ou None em caso de erro
        """
        try:
            duration = end_time - start_time
            
            # Gerar nome do arquivo se não fornecido
            if output_filename is None:
                timestamp = f"{int(start_time)}_{int(end_time)}"
                output_filename = f"clip_{timestamp}.mp4"
            
            output_path = self.output_dir / output_filename
            
            logger.info(f"Cortando vídeo: {start_time:.2f}s -> {end_time:.2f}s (duração: {duration:.2f}s)")
            
            if reencode:
                # Re-codificação (mais lento, mais preciso)
                stream = ffmpeg.input(input_video, ss=start_time, t=duration)
                stream = ffmpeg.output(
                    stream,
                    str(output_path),
                    vcodec='libx264',
                    acodec='aac',
                    preset='fast',
                    crf=23
                )
            else:
                # Stream copy (rápido, apenas copia os frames)
                stream = ffmpeg.input(input_video, ss=start_time, t=duration)
                stream = ffmpeg.output(
                    stream,
                    str(output_path),
                    vcodec='copy',
                    acodec='copy',
                    avoid_negative_ts='make_zero'
                )
            
            # Executar o comando
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            logger.info(f"Clipe salvo: {output_path}")
            return str(output_path)
            
        except ffmpeg.Error as e:
            logger.error(f"Erro do FFmpeg: {e.stderr.decode() if e.stderr else str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro ao cortar vídeo: {e}")
            return None
    
    def cut_multiple_segments(
        self,
        input_video: str,
        cut_points: List[Dict],
        prefix: str = "clip"
    ) -> List[str]:
        """
        Corta múltiplos segmentos de um vídeo
        
        Args:
            input_video: Caminho do vídeo original
            cut_points: Lista de dicionários com 'start', 'end' e opcionalmente 'reason'
            prefix: Prefixo para os nomes dos arquivos
            
        Returns:
            Lista de caminhos dos clipes gerados
        """
        output_files = []
        
        for i, cut_point in enumerate(cut_points, 1):
            start = cut_point['start']
            end = cut_point['end']
            reason = cut_point.get('reason', 'unknown')
            
            # Sanitizar o nome do arquivo
            reason_clean = self._sanitize_filename(reason)
            filename = f"{prefix}_{i:02d}_{reason_clean}.mp4"
            
            logger.info(f"Processando corte {i}/{len(cut_points)}: {reason}")
            
            output_file = self.cut_video(
                input_video=input_video,
                start_time=start,
                end_time=end,
                output_filename=filename,
                reencode=False  # Usar stream copy para velocidade
            )
            
            if output_file:
                output_files.append(output_file)
        
        logger.info(f"Concluído! {len(output_files)}/{len(cut_points)} clipes gerados")
        return output_files
    
    def _sanitize_filename(self, filename: str, max_length: int = 50) -> str:
        """Remove caracteres inválidos de nomes de arquivo"""
        # Remover caracteres especiais
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remover espaços extras
        filename = '_'.join(filename.split())
        
        # Limitar tamanho
        if len(filename) > max_length:
            filename = filename[:max_length]
        
        return filename
    
    def get_video_info(self, video_path: str) -> Optional[Dict]:
        """
        Obtém informações do vídeo (duração, resolução, codec)
        
        Args:
            video_path: Caminho do vídeo
            
        Returns:
            Dicionário com metadados do vídeo
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None
            )
            audio_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'),
                None
            )
            
            if not video_stream:
                return None
            
            duration = float(probe['format']['duration'])
            
            return {
                'duration': duration,
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'fps': eval(video_stream['r_frame_rate']),  # Ex: "30/1" -> 30.0
                'video_codec': video_stream['codec_name'],
                'audio_codec': audio_stream['codec_name'] if audio_stream else None,
                'bitrate': int(probe['format']['bit_rate']) if 'bit_rate' in probe['format'] else None,
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do vídeo: {e}")
            return None
    
    def convert_to_vertical(
        self,
        input_video: str,
        output_filename: str = None,
        target_width: int = 1080,
        target_height: int = 1920
    ) -> Optional[str]:
        """
        Converte vídeo horizontal (16:9) para vertical (9:16) usando crop centralizado
        
        Args:
            input_video: Caminho do vídeo original
            output_filename: Nome do arquivo de saída
            target_width: Largura do vídeo vertical (padrão: 1080)
            target_height: Altura do vídeo vertical (padrão: 1920)
            
        Returns:
            Caminho do vídeo vertical ou None em caso de erro
        """
        try:
            if output_filename is None:
                base = Path(input_video).stem
                output_filename = f"{base}_vertical.mp4"
            
            output_path = self.output_dir / output_filename
            
            logger.info(f"Convertendo para formato vertical ({target_width}x{target_height})")
            
            # Calcular o crop centralizado
            # Para um vídeo 1920x1080, queremos cortar para 607x1080 (9:16) e depois escalar
            info = self.get_video_info(input_video)
            if not info:
                return None
            
            original_width = info['width']
            original_height = info['height']
            
            # Calcular dimensões do crop (manter altura, ajustar largura)
            crop_width = int(original_height * (9 / 16))
            crop_x = (original_width - crop_width) // 2
            
            stream = ffmpeg.input(input_video)
            stream = ffmpeg.filter(stream, 'crop', crop_width, original_height, crop_x, 0)
            stream = ffmpeg.filter(stream, 'scale', target_width, target_height)
            stream = ffmpeg.output(
                stream,
                str(output_path),
                vcodec='libx264',
                acodec='aac',
                preset='medium',
                crf=23
            )
            
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            logger.info(f"Vídeo vertical salvo: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Erro ao converter para vertical: {e}")
            return None


# Teste do módulo
if __name__ == "__main__":
    cutter = VideoCutter(output_dir="test_clips")
    
    # Exemplo de uso
    # video_info = cutter.get_video_info("video_exemplo.mp4")
    # if video_info:
    #     print(f"Duração: {video_info['duration']}s")
    #     print(f"Resolução: {video_info['width']}x{video_info['height']}")
    
    # Cortar um segmento
    # cutter.cut_video("video_exemplo.mp4", start_time=60, end_time=120)
    
    print("Módulo de corte de vídeo carregado com sucesso!")
