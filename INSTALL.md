# Guia de Instalação e Uso - AutoClipper Bot

## 📋 Pré-requisitos

### 1. Python 3.10 ou superior
```bash
python --version  # Deve mostrar Python 3.10+
```

### 2. FFmpeg
**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

**Verificar instalação:**
```bash
ffmpeg -version
```

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/giovanisousa/ClipperBot.git
cd ClipperBot
```

### 2. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** A primeira vez que rodar o Faster-Whisper, ele vai baixar o modelo (~150MB para 'small'). Isso é normal e acontece apenas uma vez.

## 🎯 Uso Básico

### Exemplo 1: Processar vídeo do YouTube
```bash
python main_cli.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Exemplo 2: Usar palavras-chave personalizadas
```bash
python main_cli.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --keywords "milhão,segredo,atenção,incrível"
```

### Exemplo 3: Processar arquivo local
```bash
python main_cli.py \
  --file "meu_podcast.mp4" \
  --keywords "importante,revelação"
```

### Exemplo 4: Ajustar sensibilidade de volume
```bash
python main_cli.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --min-volume -15 \
  --max-clips 3
```

## 🎛️ Parâmetros Disponíveis

### Entrada
- `--url URL` - URL do vídeo do YouTube
- `--file CAMINHO` - Arquivo de vídeo local

### Análise
- `--keywords "palavra1,palavra2"` - Palavras-chave para buscar (padrão: milhão,segredo,atenção,incrível,importante)
- `--ignore "palavra1,palavra2"` - Palavras para ignorar (padrão: patrocinador,inscreva-se,anúncio)
- `--min-volume DB` - Volume mínimo em dB (padrão: -10)
- `--min-duration SEG` - Duração mínima do corte (padrão: 30)
- `--max-duration SEG` - Duração máxima do corte (padrão: 90)

### Modelo Whisper
- `--model TAMANHO` - Tamanho do modelo (tiny, base, small, medium, large-v2)
  - `tiny`: Muito rápido, menos preciso
  - `small`: **Recomendado** - Balanceado
  - `medium`: Mais preciso, mais lento
- `--language CÓDIGO` - Idioma (pt, en, es, etc)

### Saída
- `--output-dir DIRETÓRIO` - Onde salvar os clipes (padrão: output_clips)
- `--max-clips N` - Número máximo de clipes (padrão: 5)

### Opções Avançadas
- `--skip-acoustic` - Pular análise de volume (usar apenas palavras-chave)
- `--audio-only` - Baixar apenas áudio (mais rápido para testes)

## 📊 Exemplo Completo

```bash
python main_cli.py \
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --keywords "never,gonna,give,up" \
  --ignore "advertisement" \
  --min-volume -12 \
  --min-duration 25 \
  --max-duration 60 \
  --model small \
  --language en \
  --output-dir my_clips \
  --max-clips 3
```

## 🐛 Solução de Problemas

### Erro: "FFmpeg não encontrado"
Instale o FFmpeg conforme instruções acima.

### Erro: "CUDA not available" ou muito lento
Isso é normal em CPUs. O Faster-Whisper funciona bem sem GPU. Use `--model small` ou `--model tiny` para mais velocidade.

### Erro de memória
Use um modelo menor: `--model tiny` ou `--model base`

### Download muito lento
Use `--audio-only` para baixar apenas o áudio (mais rápido).

## 📁 Estrutura de Saída

```
output_clips/
├── autoclipper_01_keyword_milhão.mp4
├── autoclipper_02_volume_peak_12.5dB.mp4
└── autoclipper_03_keyword_segredo.mp4
```

## 🔄 Próximos Passos (Branches Futuras)

- **Branch 02**: Interface gráfica (GUI)
- **Branch 03**: Perfis configuráveis (JSON)
- **Branch 04**: Sistema de autenticação
- **Branch 05**: Corte vertical (9:16) e legendas
- **Branch 06**: Instalador executável

## 💡 Dicas de Performance

1. **Use o modelo 'small'**: Melhor custo-benefício velocidade/precisão
2. **Limite o número de clipes**: `--max-clips 3` gera resultados mais rápido
3. **Processe offline**: Baixe o vídeo primeiro, depois processe localmente
4. **Ajuste sensibilidade**: Valores muito baixos de `--min-volume` geram muitos falsos positivos

## 📞 Suporte

Para problemas ou dúvidas, abra uma issue no GitHub:
https://github.com/giovanisousa/ClipperBot/issues
