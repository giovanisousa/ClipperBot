#!/bin/bash
# Script de exemplo para processar vídeo do Flow Podcast

echo "🎬 AutoClipper Bot - Exemplo Flow Podcast"
echo "=========================================="
echo ""

# URL de exemplo (substitua pela URL real)
VIDEO_URL="https://www.youtube.com/watch?v=EXAMPLE"

# Configurações do perfil Flow
KEYWORDS="incrível,surpreendente,polêmico,controverso,sinceramente,verdade,revelação"
IGNORE="patrocinador,inscreva-se,cortes"
MIN_VOLUME=-12
MIN_DURATION=45
MAX_DURATION=120
MAX_CLIPS=7

echo "📋 Configurações:"
echo "  - Palavras-chave: $KEYWORDS"
echo "  - Volume mínimo: ${MIN_VOLUME}dB"
echo "  - Duração: ${MIN_DURATION}s - ${MAX_DURATION}s"
echo "  - Máximo de clipes: $MAX_CLIPS"
echo ""

read -p "Digite a URL do vídeo do YouTube: " VIDEO_URL

if [ -z "$VIDEO_URL" ]; then
    echo "❌ URL não fornecida"
    exit 1
fi

echo ""
echo "🚀 Iniciando processamento..."
echo ""

python main_cli.py \
    --url "$VIDEO_URL" \
    --keywords "$KEYWORDS" \
    --ignore "$IGNORE" \
    --min-volume "$MIN_VOLUME" \
    --min-duration "$MIN_DURATION" \
    --max-duration "$MAX_DURATION" \
    --max-clips "$MAX_CLIPS" \
    --model small \
    --language pt \
    --output-dir "clips_flow"

echo ""
echo "✅ Processamento concluído!"
echo "📁 Clipes salvos em: clips_flow/"
