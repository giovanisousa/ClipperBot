# 🎬 AutoClipper Bot

**Sistema de automação para cortes inteligentes de vídeos longos** (podcasts, palestras, lives).

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()
[![Status](https://img.shields.io/badge/Status-Branch%2001%20Complete-brightgreen.svg)]()

---

## 📋 Visão Geral

O **AutoClipper Bot** processa vídeos **localmente** na sua máquina, utilizando:
- 🎤 **Transcrição automática** (Faster-Whisper)
- 🔍 **Análise semântica** (palavras-chave)
- 🔊 **Análise acústica** (picos de volume)
- ✂️ **Corte automatizado** (FFmpeg)

**Resultado:** Gere automaticamente 5-10 clipes prontos para TikTok/Reels a partir de um vídeo longo!

### ✨ Diferenciais

- ✅ **100% Local**: Sem enviar dados para APIs externas
- ✅ **Sem IA Visual**: Usa apenas áudio (mais rápido e leve)
- ✅ **CPU-Friendly**: Funciona sem placa de vídeo dedicada
- ✅ **Open Architecture**: Código modular e extensível

## 🚀 Roadmap de Desenvolvimento

| Branch | Status | Descrição | Entregáveis |
|--------|--------|-----------|-------------|
| **01** | ✅ **COMPLETO** | Core Engine POC | CLI funcional, 4 módulos principais |
| **02** | 📅 Planejado | Interface Gráfica | GUI com CustomTkinter |
| **03** | 📅 Planejado | Perfis JSON | Sistema de configuração |
| **04** | 📅 Planejado | Autenticação | Anti-pirataria + Login |
| **05** | 📅 Planejado | Refinamento | Corte 9:16 + Legendas |
| **06** | 📅 Planejado | Distribuição | Instalador .exe |

### 🎯 Branch Atual: 01 - Core Engine POC

**O que funciona:**
- ✅ Download de vídeos do YouTube
- ✅ Transcrição com timestamps precisos
- ✅ Identificação de clímax (semântica + acústica)
- ✅ Corte automatizado em lote
- ✅ Interface CLI completa

**Próximo passo:** Branch 02 (Interface Gráfica)

## 🛠️ Stack Tecnológica

- **Python 3.10+**
- **yt-dlp** - Download de vídeos
- **faster-whisper** - Transcrição local
- **FFmpeg** - Processamento de vídeo/áudio
- **librosa/pydub** - Análise de áudio
- **CustomTkinter** - Interface gráfica (futuro)

## 📦 Instalação (Dev)

## 🚀 Início Rápido

### 1️⃣ Instalação

```bash
# Clonar repositório
git clone https://github.com/giovanisousa/ClipperBot.git
cd ClipperBot

# Criar ambiente virtual
## 📁 Estrutura do Projeto

```
ClipperBot/
├── src/                      # 🧠 Módulos principais
│   ├── downloader.py         # Download (yt-dlp)
│   ├── transcriber.py        # Transcrição (Faster-Whisper)
│   ├── analyzer.py           # Análise de clímax
│   └── video_cutter.py       # Corte (FFmpeg)
├── examples/                 # 📋 Exemplos e perfis
│   ├── profile_marcal.json   # Perfil negócios
│   ├── profile_flow.json     # Perfil podcast
│   └── profile_humor.json    # Perfil comédia
├── main_cli.py              # 🖥️ Interface CLI
├── test_environment.py      # 🧪 Teste de ambiente
├── requirements.txt         # 📦 Dependências
├── INSTALL.md              # 📚 Guia de instalação
├── BRANCH_01_SUMMARY.md    # 📊 Resumo da Branch 01
└── README.md               # 📖 Este arquivo
```

## 🎓 Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **yt-dlp** | Download de vídeos do YouTube |
| **Faster-Whisper** | Transcrição Speech-to-Text (local) |
| **FFmpeg** | Processamento e corte de vídeo |
| **librosa** | Análise de áudio (volume/energia) |
| **Python 3.10+** | Linguagem base |

## 📊 Performance

- ⏱️ **Transcrição**: ~2-3x tempo real (CPU moderna)
- ⚡ **Corte**: Instantâneo (stream copy)
- 💾 **RAM**: 2-4 GB durante processamento
- 🎯 **Precisão**: 85-95% (modelo small)

## 🤝 Contribuindo

Este projeto está em desenvolvimento ativo. Sugestões e feedback são bem-vindos!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

- 📖 **Documentação**: [INSTALL.md](INSTALL.md), [BRANCH_01_SUMMARY.md](BRANCH_01_SUMMARY.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/giovanisousa/ClipperBot/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/giovanisousa/ClipperBot/discussions)

## 📄 Licença

**Proprietary** - Todos os direitos reservados.

Este software está em desenvolvimento e não possui licença de código aberto no momento.

---

**Desenvolvido com ❤️ para economizar horas de edição de vídeo!**

⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!
# Processar vídeo do YouTube
python main_cli.py --url "https://youtube.com/watch?v=VIDEO_ID"

# Com configurações personalizadas
python main_cli.py \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --keywords "milhão,segredo,atenção" \
  --max-clips 5 \
  --min-volume -10
```

### 3️⃣ Ver Resultados

```bash
# Clipes gerados em:
ls output_clips/

# Exemplo de saída:
# autoclipper_01_keyword_milhão.mp4
# autoclipper_02_volume_peak_12.5dB.mp4
# autoclipper_03_keyword_segredo.mp4
```

📚 **Documentação completa:** [INSTALL.md](INSTALL.md)📁 Estrutura do Projeto

```
ClipperBot/
├── src/
│   ├── downloader.py      # Download de vídeos
│   ├── transcriber.py     # Transcrição de áudio
│   ├── analyzer.py        # Análise de clímax
│   └── video_cutter.py    # Corte de vídeos
├── main_cli.py            # Interface de linha de comando
├── requirements.txt       # Dependências
└── README.md
```

## 📄 Licença

Proprietary - Todos os direitos reservados
