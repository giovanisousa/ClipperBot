# Exemplos de Uso - AutoClipper Bot

Este diretório contém exemplos práticos e perfis de configuração para diferentes tipos de conteúdo.

## 📋 Perfis de Configuração (JSON)

### 1. `profile_marcal.json`
Otimizado para conteúdo motivacional e de negócios (estilo Pablo Marçal).
- Foco em palavras como "milhão", "estratégia", "sucesso"
- Cortes de 30-90 segundos
- Volume mínimo: -10dB

### 2. `profile_flow.json`
Otimizado para podcasts longos e entrevistas (estilo Flow Podcast).
- Foco em momentos de revelação e histórias interessantes
- Cortes de 45-120 segundos
- Volume mínimo: -12dB

### 3. `profile_humor.json`
Otimizado para capturar momentos engraçados e risadas.
- Foco em palavras como "kkk", "engraçado", "piada"
- Cortes curtos de 20-60 segundos
- Volume mínimo: -8dB (para capturar risadas altas)

## 🚀 Scripts de Exemplo

### `run_flow_example.sh`
Script bash para processar vídeos com o perfil Flow Podcast.

**Uso:**
```bash
chmod +x examples/run_flow_example.sh
./examples/run_flow_example.sh
```

## 💡 Como Usar os Perfis (Branch 03)

**Nota:** Os perfis JSON são preparatórios para a Branch 03. Na Branch 01 (atual), você deve passar as configurações via argumentos CLI.

**Exemplo equivalente ao perfil Flow:**
```bash
python main_cli.py \
  --url "https://youtube.com/watch?v=..." \
  --keywords "incrível,surpreendente,polêmico,controverso,sinceramente,verdade,revelação" \
  --ignore "patrocinador,inscreva-se,cortes" \
  --min-volume -12 \
  --min-duration 45 \
  --max-duration 120 \
  --max-clips 7 \
  --output-dir "clips_flow"
```

## 📝 Criar Seu Próprio Perfil

1. Copie um dos arquivos JSON de exemplo
2. Edite as palavras-chave para seu nicho
3. Ajuste as durações e sensibilidade
4. Converta para argumentos CLI (Branch 01) ou use diretamente (Branch 03+)

### Estrutura do Perfil JSON

```json
{
  "name": "Nome do Perfil",
  "description": "Descrição do uso",
  "settings": {
    "keywords_climax": ["palavra1", "palavra2"],
    "keywords_ignore": ["palavra3", "palavra4"],
    "audio_analysis": {
      "min_volume_db": -10.0,
      "enable_acoustic": true
    },
    "cut_settings": {
      "min_duration": 30,
      "max_duration": 90,
      "pre_roll": 5,
      "post_roll": 5
    },
    "transcription": {
      "model_size": "small",
      "language": "pt"
    },
    "output": {
      "max_clips": 5,
      "prefix": "meu_perfil"
    }
  }
}
```

## 🎯 Dicas de Configuração

### Palavras-chave
- **Específicas**: "milhão", "bilhão" (nichos de negócios)
- **Genéricas**: "incrível", "importante" (geral)
- **Emocionais**: "kkk", "risada" (comédia)

### Volume (dB)
- **-8dB**: Apenas momentos MUITO altos (risadas, gritos)
- **-10dB**: Momentos de euforia (recomendado)
- **-12dB**: Conversas animadas
- **-15dB**: Conversas normais

### Duração
- **Curta (20-60s)**: TikTok, Instagram Reels
- **Média (30-90s)**: YouTube Shorts, Twitter
- **Longa (60-120s)**: LinkedIn, Facebook

## 📊 Comparação de Perfis

| Perfil | Nicho | Duração Média | Volume | Clips/Vídeo |
|--------|-------|---------------|--------|-------------|
| Marçal | Negócios | 30-90s | -10dB | 5 |
| Flow | Podcast | 45-120s | -12dB | 7 |
| Humor | Comédia | 20-60s | -8dB | 10 |

## 🔄 Iteração e Ajustes

1. **Primeira execução**: Use configurações padrão
2. **Analise os resultados**: Os clipes capturaram o que você queria?
3. **Ajuste**: Se muitos falsos positivos, aumente o volume mínimo ou seja mais específico nas palavras
4. **Teste novamente**: Itere até encontrar o ponto ideal

## 📞 Feedback

Se criar um perfil interessante, compartilhe! Abra uma issue ou PR no GitHub.
