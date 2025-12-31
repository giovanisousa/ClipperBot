"""
Módulo de Transcrição de Áudio
Utiliza Faster-Whisper para converter áudio em texto com timestamps precisos
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from faster_whisper import WhisperModel
from src.cache import TranscriptionCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioTranscriber:
    """
    Gerencia a transcrição de áudio usando Faster-Whisper
    """
    
    def __init__(
        self, 
        model_size: str = "small",
        device: str = "auto",
        compute_type: str = "auto",
        use_cache: bool = True
    ):
        """
        Args:
            model_size: Tamanho do modelo (tiny, base, small, medium, large-v2)
                       - tiny: muito rápido, menos preciso
                       - small: balanceado (RECOMENDADO)
                       - medium: mais preciso, mais lento
            device: "cpu", "cuda" ou "auto" (detecta automaticamente)
            compute_type: "int8", "float16" ou "auto"
            use_cache: Se True, usa cache de transcrições (economiza tempo)
        """
        self.model_size = model_size
        self.use_cache = use_cache
        
        if use_cache:
            self.cache = TranscriptionCache()
        else:
            self.cache = None
        
        # Detectar dispositivo automaticamente
        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
            logger.info(f"Dispositivo detectado: {device}")
        
        # Otimizar compute_type baseado no dispositivo
        if compute_type == "auto":
            compute_type = "float16" if device == "cuda" else "int8"
        
        logger.info(f"Carregando modelo Whisper '{model_size}' ({device}, {compute_type})")
        
        try:
            self.model = WhisperModel(
                model_size,
                device=device,
                compute_type=compute_type
            )
            logger.info("✓ Modelo carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise
    
    def transcribe(
        self, 
        audio_path: str,
        language: str = "pt",
        word_timestamps: bool = True
    ) -> Optional[List[Dict]]:
        """
        Transcreve o áudio completo com timestamps
        
        Args:
            audio_path: Caminho do arquivo de áudio
            language: Código do idioma (pt, en, es, etc)
            word_timestamps: Se True, retorna timestamp de cada palavra
            
        Returns:
            Lista de segmentos com texto e timestamps
        """
        if not Path(audio_path).exists():
            logger.error(f"Arquivo não encontrado: {audio_path}")
            return None
        
        # Verificar cache
        if self.cache:
            cached = self.cache.get(audio_path, self.model_size, language)
            if cached:
                logger.info("⚡ Usando transcrição do cache (economia de tempo!)")
                return cached
        
        try:
            logger.info(f"Transcrevendo: {audio_path}")
            
            segments, info = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=word_timestamps,
                vad_filter=True,  # Voice Activity Detection (remove silêncios)
                beam_size=5,      # Aumenta precisão
            )
            
            logger.info(f"Idioma detectado: {info.language} (confiança: {info.language_probability:.2%})")
            
            # Converter generator em lista de dicionários
            transcription = []
            for segment in segments:
                segment_dict = {
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                }
                
                # Incluir timestamps de palavras individuais se solicitado
                if word_timestamps and hasattr(segment, 'words'):
                    segment_dict['words'] = [
                        {
                            'word': word.word.strip(),
                            'start': word.start,
                            'end': word.end,
                        }
                        for word in segment.words
                    ]
                
                transcription.append(segment_dict)
                
                # Log de progresso
                logger.debug(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text.strip()}")
            
            logger.info(f"Transcrição concluída: {len(transcription)} segmentos")
            
            # Salvar no cache
            if self.cache:
                self.cache.set(audio_path, transcription, self.model_size, language)
            
            return transcription
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            return None
    
    def transcribe_segment(
        self, 
        audio_path: str, 
        start_time: float, 
        end_time: float,
        language: str = "pt"
    ) -> Optional[str]:
        """
        Transcreve apenas um segmento específico do áudio
        
        Args:
            audio_path: Caminho do arquivo de áudio
            start_time: Início do segmento (segundos)
            end_time: Fim do segmento (segundos)
            language: Código do idioma
            
        Returns:
            Texto do segmento transcrito
        """
        # Para transcrever apenas um segmento, precisaríamos cortar o áudio primeiro
        # Por simplicidade, vamos transcrever tudo e filtrar
        full_transcription = self.transcribe(audio_path, language, word_timestamps=False)
        
        if not full_transcription:
            return None
        
        # Filtrar segmentos que estão no intervalo desejado
        segment_texts = [
            seg['text'] 
            for seg in full_transcription 
            if seg['start'] >= start_time and seg['end'] <= end_time
        ]
        
        return " ".join(segment_texts)
    
    def get_full_text(self, transcription: List[Dict]) -> str:
        """
        Retorna o texto completo concatenado (sem timestamps)
        
        Args:
            transcription: Lista de segmentos retornada por transcribe()
            
        Returns:
            Texto completo
        """
        return " ".join([seg['text'] for seg in transcription])
    
    def search_keyword_timestamps(
        self, 
        transcription: List[Dict], 
        keywords: List[str]
    ) -> List[Tuple[str, float, float]]:
        """
        Busca palavras-chave na transcrição e retorna os timestamps
        
        Args:
            transcription: Lista de segmentos retornada por transcribe()
            keywords: Lista de palavras-chave para buscar (case-insensitive)
            
        Returns:
            Lista de tuplas (keyword, start_time, end_time) onde a palavra foi encontrada
        """
        matches = []
        
        for segment in transcription:
            text_lower = segment['text'].lower()
            
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matches.append((
                        keyword,
                        segment['start'],
                        segment['end']
                    ))
                    logger.info(f"Encontrado '{keyword}' em [{segment['start']:.2f}s - {segment['end']:.2f}s]")
        
        return matches


# Teste do módulo
if __name__ == "__main__":
    # Exemplo de uso
    transcriber = AudioTranscriber(model_size="small")
    
    # Para testar, você precisaria de um arquivo de áudio
    # transcription = transcriber.transcribe("audio_exemplo.wav", language="pt")
    
    # Exemplo de busca de palavras-chave
    # keywords = ["milhão", "segredo", "atenção"]
    # matches = transcriber.search_keyword_timestamps(transcription, keywords)
    
    print("Módulo de transcrição carregado com sucesso!")
    print(f"Modelo: {transcriber.model_size}")
