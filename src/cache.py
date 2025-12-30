"""
Sistema de Cache para Transcrições
Evita re-processar o mesmo áudio múltiplas vezes
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptionCache:
    """
    Gerencia cache de transcrições para evitar re-processar os mesmos arquivos
    """
    
    def __init__(self, cache_dir: str = ".cache_transcriptions"):
        """
        Args:
            cache_dir: Diretório onde os caches serão salvos
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_hash(self, file_path: str) -> str:
        """
        Gera hash único do arquivo baseado em nome, tamanho e data de modificação
        (mais rápido que hash do conteúdo completo)
        """
        path = Path(file_path)
        if not path.exists():
            return ""
        
        stat = path.stat()
        hash_input = f"{path.name}_{stat.st_size}_{stat.st_mtime}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _get_cache_path(self, file_hash: str, model_size: str, language: str) -> Path:
        """Retorna o caminho do arquivo de cache"""
        cache_filename = f"{file_hash}_{model_size}_{language}.json"
        return self.cache_dir / cache_filename
    
    def get(
        self, 
        audio_path: str, 
        model_size: str = "small", 
        language: str = "pt"
    ) -> Optional[List[Dict]]:
        """
        Busca transcrição no cache
        
        Args:
            audio_path: Caminho do arquivo de áudio
            model_size: Tamanho do modelo usado
            language: Idioma da transcrição
            
        Returns:
            Lista de segmentos transcritos ou None se não encontrado
        """
        file_hash = self._get_file_hash(audio_path)
        if not file_hash:
            return None
        
        cache_path = self._get_cache_path(file_hash, model_size, language)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"✅ Transcrição encontrada no cache: {cache_path.name}")
                return data['transcription']
            except Exception as e:
                logger.warning(f"Erro ao ler cache: {e}")
                return None
        
        return None
    
    def set(
        self, 
        audio_path: str, 
        transcription: List[Dict], 
        model_size: str = "small", 
        language: str = "pt"
    ) -> bool:
        """
        Salva transcrição no cache
        
        Args:
            audio_path: Caminho do arquivo de áudio
            transcription: Lista de segmentos transcritos
            model_size: Tamanho do modelo usado
            language: Idioma da transcrição
            
        Returns:
            True se salvou com sucesso
        """
        file_hash = self._get_file_hash(audio_path)
        if not file_hash:
            return False
        
        cache_path = self._get_cache_path(file_hash, model_size, language)
        
        try:
            cache_data = {
                'file_path': str(audio_path),
                'model_size': model_size,
                'language': language,
                'transcription': transcription
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Transcrição salva no cache: {cache_path.name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {e}")
            return False
    
    def clear(self, audio_path: Optional[str] = None):
        """
        Limpa cache
        
        Args:
            audio_path: Se fornecido, limpa apenas cache deste arquivo.
                       Se None, limpa todo o cache.
        """
        if audio_path:
            file_hash = self._get_file_hash(audio_path)
            if file_hash:
                # Remover todos os caches deste arquivo (diferentes modelos/idiomas)
                for cache_file in self.cache_dir.glob(f"{file_hash}_*.json"):
                    cache_file.unlink()
                    logger.info(f"🗑️ Cache removido: {cache_file.name}")
        else:
            # Limpar todo o cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("🗑️ Todo o cache foi limpo")
    
    def list_cached_files(self) -> List[Dict]:
        """
        Lista todos os arquivos em cache
        
        Returns:
            Lista de dicionários com informações dos caches
        """
        cached_files = []
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                cached_files.append({
                    'cache_file': cache_file.name,
                    'original_file': data.get('file_path', 'unknown'),
                    'model_size': data.get('model_size', 'unknown'),
                    'language': data.get('language', 'unknown'),
                    'size_kb': cache_file.stat().st_size / 1024
                })
            except Exception:
                pass
        
        return cached_files
    
    def get_cache_size(self) -> float:
        """
        Retorna tamanho total do cache em MB
        """
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))
        return total_size / (1024 * 1024)


# Teste do módulo
if __name__ == "__main__":
    cache = TranscriptionCache()
    
    # Listar caches
    cached = cache.list_cached_files()
    print(f"Arquivos em cache: {len(cached)}")
    print(f"Tamanho total: {cache.get_cache_size():.2f} MB")
    
    for item in cached:
        print(f"  - {item['cache_file']}: {item['size_kb']:.1f} KB")
