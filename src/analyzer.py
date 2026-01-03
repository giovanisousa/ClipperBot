"""
Módulo de Análise de Clímax
Combina análise semântica (palavras-chave) e acústica (volume/energia) para identificar momentos relevantes
"""

import logging
from typing import List, Dict, Tuple, Optional
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimaxAnalyzer:
    """
    Identifica pontos de clímax em vídeos combinando:
    - Análise semântica: palavras-chave na transcrição
    - Análise acústica: picos de volume, mudanças de energia
    """
    
    # Pesos padrão para palavras-chave (maior peso = maior prioridade)
    DEFAULT_KEYWORD_WEIGHTS = {
        # Palavras de alto impacto
        'burro': 3.0,
        'dinheiro': 3.0,
        'segredo': 3.0,
        'lula': 3.0,
        'brasil': 3.0,
        'milhão': 2.5,
        'bilhão': 2.5,
        'importante': 2.5,
        'incrível': 2.0,
        'nunca': 2.0,
        'sempre': 2.0,
        'prosperar': 2.0,
        # Palavras genéricas (menor prioridade)
        'atenção': 1.0,
        'olha': 1.0,
        'veja': 1.0,
    }
    
    def __init__(
        self,
        keywords_climax: List[str],
        keywords_ignore: List[str] = None,
        keyword_weights: Dict[str, float] = None,
        min_volume_db: float = -10.0,
        cut_duration_min: int = 30,
        cut_duration_max: int = 90,
        pre_roll: int = 5,
        post_roll: int = 5,
        safety_margin: int = 8
    ):
        """
        Args:
            keywords_climax: Palavras que indicam momentos interessantes
            keywords_ignore: Palavras que indicam trechos a evitar (patrocinador, etc)
            keyword_weights: Dicionário com pesos customizados para palavras-chave
            min_volume_db: Volume mínimo para considerar "euforia" (ex: -10db)
            cut_duration_min: Duração mínima do corte (segundos)
            cut_duration_max: Duração máxima do corte (segundos)
            pre_roll: Segundos antes do ponto de interesse (contexto)
            post_roll: Segundos após o ponto de interesse (contexto)
            safety_margin: Margem de segurança adicional no final (segundos)
        """
        self.keywords_climax = [k.lower() for k in keywords_climax]
        self.keywords_ignore = [k.lower() for k in (keywords_ignore or [])]
        
        # Mesclar pesos customizados com pesos padrão
        self.keyword_weights = self.DEFAULT_KEYWORD_WEIGHTS.copy()
        if keyword_weights:
            self.keyword_weights.update({k.lower(): v for k, v in keyword_weights.items()})
        
        self.min_volume_db = min_volume_db
        self.cut_duration_min = cut_duration_min
        self.cut_duration_max = cut_duration_max
        self.pre_roll = pre_roll
        self.post_roll = post_roll
        self.safety_margin = safety_margin
    
    def analyze_semantic(self, transcription: List[Dict]) -> List[Dict]:
        """
        Analisa a transcrição buscando palavras-chave de clímax
        
        Args:
            transcription: Lista de segmentos da transcrição
            
        Returns:
            Lista de momentos interessantes encontrados:
            [
                {
                    'type': 'semantic',
                    'keyword': 'milhão',
                    'start': 125.5,
                    'end': 130.2,
                    'text': 'Eu ganhei um milhão de reais',
                    'weight': 2.5
                },
                ...
            ]
        """
        climax_moments = []
        
        for i, segment in enumerate(transcription):
            text_lower = segment['text'].lower()
            
            # Verificar se contém palavras a ignorar
            should_ignore = any(ignore_word in text_lower for ignore_word in self.keywords_ignore)
            if should_ignore:
                logger.debug(f"Ignorando segmento (palavra de exclusão): {segment['text'][:50]}...")
                continue
            
            # Verificar se contém palavras de clímax
            for keyword in self.keywords_climax:
                if keyword in text_lower:
                    # Obter peso da palavra-chave (padrão 1.0)
                    weight = self.keyword_weights.get(keyword, 1.0)
                    
                    # Estender o segmento até o final da frase completa
                    extended_end = self._find_sentence_end(transcription, i)
                    
                    climax_moments.append({
                        'type': 'semantic',
                        'keyword': keyword,
                        'start': segment['start'],
                        'end': extended_end,
                        'text': segment['text'],
                        'score': weight,  # Score baseado no peso da palavra
                        'weight': weight,
                        'complete_sentence': True
                    })
                    logger.info(f"Clímax semântico encontrado: '{keyword}' (peso: {weight}) em {segment['start']:.2f}s")
        
        return climax_moments
    
    def _find_sentence_end(self, transcription: List[Dict], start_idx: int) -> float:
        """
        Encontra o final da frase completa a partir do segmento inicial.
        Busca por pontos finais (. ! ?) e evita terminar em vírgulas.
        
        Args:
            transcription: Lista completa de segmentos
            start_idx: Índice do segmento inicial
            
        Returns:
            Timestamp do final da frase completa
        """
        # Caracteres que indicam fim de frase
        sentence_endings = ['.', '!', '?']
        
        # Começar do segmento atual
        for i in range(start_idx, len(transcription)):
            text = transcription[i]['text']
            
            # Verificar se termina com pontuação de fim de frase
            if any(text.rstrip().endswith(ending) for ending in sentence_endings):
                return transcription[i]['end']
            
            # Limite de busca: não avançar mais de 3 segmentos (evitar frases muito longas)
            if i - start_idx >= 3:
                return transcription[i]['end']
        
        # Se não encontrar, retornar o fim do segmento inicial
        return transcription[start_idx]['end']
    
    def analyze_acoustic(self, audio_path: str, sample_window: int = 5, fast_mode: bool = True) -> List[Dict]:
        """
        Analisa o áudio buscando picos de volume e energia
        
        Args:
            audio_path: Caminho do arquivo de áudio
            sample_window: Janela de análise em segundos
            fast_mode: Se True, usa downsampling para análise mais rápida
            
        Returns:
            Lista de momentos com alta energia acústica
        """
        try:
            logger.info(f"Analisando áudio: {audio_path}")
            
            # Carregar áudio com librosa (downsampling para 8kHz se fast_mode)
            target_sr = 8000 if fast_mode else None  # 8kHz é suficiente para análise de volume
            y, sr = librosa.load(audio_path, sr=target_sr)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Calcular energia RMS (Root Mean Square) - indica volume
            rms = librosa.feature.rms(y=y)[0]
            
            # Converter RMS para dB
            rms_db = librosa.amplitude_to_db(rms)
            
            # Calcular timestamps para cada frame RMS
            frames = range(len(rms))
            times = librosa.frames_to_time(frames, sr=sr)
            
            # Identificar picos de energia
            climax_moments = []
            threshold_db = self.min_volume_db
            
            for i, (time, db) in enumerate(zip(times, rms_db)):
                if db > threshold_db:
                    # Agrupar picos próximos
                    start_time = max(0, time - sample_window / 2)
                    end_time = min(duration, time + sample_window / 2)
                    
                    climax_moments.append({
                        'type': 'acoustic',
                        'start': float(start_time),
                        'end': float(end_time),
                        'peak_db': float(db),
                        'score': float((db - threshold_db) / 10)  # Score normalizado
                    })
            
            # Remover duplicatas (picos muito próximos)
            climax_moments = self._merge_overlapping_moments(climax_moments)
            
            logger.info(f"Encontrados {len(climax_moments)} picos acústicos")
            return climax_moments
            
        except Exception as e:
            logger.error(f"Erro na análise acústica: {e}")
            return []
    
    def _merge_overlapping_moments(self, moments: List[Dict], min_gap: float = 10.0) -> List[Dict]:
        """
        Mescla momentos que estão muito próximos um do outro
        
        Args:
            moments: Lista de momentos
            min_gap: Distância mínima entre momentos (segundos)
            
        Returns:
            Lista de momentos mesclados
        """
        if not moments:
            return []
        
        # Ordenar por tempo de início
        moments = sorted(moments, key=lambda x: x['start'])
        
        merged = [moments[0]]
        
        for current in moments[1:]:
            last = merged[-1]
            
            # Se os momentos estão próximos, mesclar
            if current['start'] - last['end'] < min_gap:
                last['end'] = max(last['end'], current['end'])
                # Manter o maior score
                if 'score' in current and 'score' in last:
                    last['score'] = max(last['score'], current['score'])
            else:
                merged.append(current)
        
        return merged
    
    def combine_analyses(
        self, 
        semantic_moments: List[Dict], 
        acoustic_moments: List[Dict]
    ) -> List[Dict]:
        """
        Combina análises semântica e acústica, priorizando momentos que aparecem em ambas
        
        Args:
            semantic_moments: Momentos encontrados na análise de texto
            acoustic_moments: Momentos encontrados na análise de áudio
            
        Returns:
            Lista unificada e ranqueada de momentos de clímax
        """
        combined = []
        
        # Adicionar todos os momentos semânticos (alta prioridade)
        for sem_moment in semantic_moments:
            moment = sem_moment.copy()
            moment['priority'] = 'high'
            
            # Verificar se há sobreposição com picos acústicos
            for ac_moment in acoustic_moments:
                if self._moments_overlap(sem_moment, ac_moment):
                    moment['priority'] = 'very_high'  # Combinação perfeita!
                    moment['acoustic_boost'] = ac_moment.get('peak_db', 0)
                    logger.info(f"🔥 CLÍMAX COMBINADO em {moment['start']:.2f}s: '{moment.get('keyword', '')}'")
                    break
            
            combined.append(moment)
        
        # Adicionar momentos acústicos que não sobrepõem com semânticos
        for ac_moment in acoustic_moments:
            has_overlap = any(self._moments_overlap(ac_moment, sem) for sem in semantic_moments)
            if not has_overlap:
                moment = ac_moment.copy()
                moment['priority'] = 'medium'
                combined.append(moment)
        
        # Ordenar por prioridade e score
        priority_order = {'very_high': 3, 'high': 2, 'medium': 1}
        combined.sort(
            key=lambda x: (priority_order.get(x.get('priority', 'medium'), 0), x.get('score', 0)),
            reverse=True
        )
        
        return combined
    
    def _moments_overlap(self, moment1: Dict, moment2: Dict) -> bool:
        """Verifica se dois momentos se sobrepõem no tempo"""
        return not (moment1['end'] < moment2['start'] or moment2['end'] < moment1['start'])
    
    def create_cut_points(self, climax_moments: List[Dict]) -> List[Dict]:
        """
        Converte momentos de clímax em pontos de corte com duração adequada
        
        Args:
            climax_moments: Lista de momentos identificados
            
        Returns:
            Lista de pontos de corte prontos para extração:
            [
                {
                    'start': 120.0,
                    'end': 180.0,
                    'duration': 60,
                    'reason': 'keyword: milhão',
                    'priority': 'very_high',
                    'weight': 2.5
                },
                ...
            ]
        """
        cut_points = []
        
        for moment in climax_moments:
            # Aplicar pre-roll e post-roll + margem de segurança
            start = max(0, moment['start'] - self.pre_roll)
            # AJUSTE CRÍTICO: Adicionar margem de segurança no final
            end = moment['end'] + self.post_roll + self.safety_margin
            duration = end - start
            
            # Ajustar para respeitar duração mínima/máxima
            if duration < self.cut_duration_min:
                # Expandir simetricamente
                expansion = (self.cut_duration_min - duration) / 2
                start = max(0, start - expansion)
                end = end + expansion
                duration = end - start
            
            if duration > self.cut_duration_max:
                # Truncar mantendo o final (prioridade para não cortar a conclusão)
                start = end - self.cut_duration_max
                duration = self.cut_duration_max
            
            # Criar descrição do motivo do corte
            weight = moment.get('weight', 1.0)
            reason = moment.get('keyword', moment.get('type', 'unknown'))
            if moment.get('type') == 'semantic':
                reason = f"keyword: {moment.get('keyword', '')} (peso: {weight})"
            elif moment.get('type') == 'acoustic':
                reason = f"volume peak: {moment.get('peak_db', 0):.1f}dB"
            
            cut_points.append({
                'start': float(start),
                'end': float(end),
                'duration': float(duration),
                'reason': reason,
                'priority': moment.get('priority', 'medium'),
                'text': moment.get('text', ''),
                'weight': weight,
                'complete_sentence': moment.get('complete_sentence', False)
            })
        
        logger.info(f"Criados {len(cut_points)} pontos de corte")
        return cut_points


# Teste do módulo
if __name__ == "__main__":
    # Exemplo de configuração
    analyzer = ClimaxAnalyzer(
        keywords_climax=["milhão", "segredo", "atenção", "incrível"],
        keywords_ignore=["patrocinador", "inscreva-se", "anúncio"],
        min_volume_db=-10.0,
        cut_duration_min=30,
        cut_duration_max=90
    )
    
    print("Analisador de clímax configurado!")
    print(f"Palavras-chave: {analyzer.keywords_climax}")
    print(f"Volume mínimo: {analyzer.min_volume_db}dB")
