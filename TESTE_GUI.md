# 🚀 Teste Rápido da GUI Integrada

## Como Testar

### 1. Ativar Ambiente
```powershell
.\.venv\Scripts\Activate.ps1
$env:Path += ";C:\Users\Giovani Souza\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
```

### 2. Executar GUI
```powershell
python gui_main.py
```

### 3. Fluxo de Teste

#### Teste Básico:
1. **URL do YouTube**: Cole uma URL curta (2-5 min recomendado para teste)
2. **Palavras-chave**: Clique em "📋 Padrão" para carregar palavras sugeridas
3. **Configurações**:
   - Modelo: `tiny` (mais rápido)
   - Número de Clipes: `3`
   - Modo Rápido: ✅ Ativado
   - Margem de Segurança: `8s`
4. **Processar**: Clique em "🚀 Processar Vídeo"

#### Teste com Palavras Customizadas:
1. Digite uma palavra-chave no campo
2. Ajuste o peso usando o slider (1.0 a 3.0)
3. Clique em ➕ para adicionar
4. Repita para múltiplas palavras

#### Teste com Arquivo Local:
1. Selecione "Arquivo Local"
2. Clique em 📁 para selecionar um vídeo MP4
3. Configure e processe

### 4. Acompanhar Progresso

#### Aba Status:
- Veja o status atual
- Barra de progresso visual
- Informações em tempo real

#### Aba Logs:
- Log detalhado de cada etapa
- Mensagens de erro (se houver)
- Estatísticas do processamento

#### Aba Resultados:
- Lista de clipes gerados
- Tamanho de cada arquivo
- Botões para abrir pasta ou reproduzir

### 5. Verificar Resultados

**Pasta de Saída**: `output_clips_YYYYMMDD_HHMMSS`

**Ações Disponíveis**:
- **📂 Abrir Pasta**: Abre a pasta com os clipes
- **▶️ Reproduzir**: Reproduz o clipe selecionado

---

## 🧪 Testes Recomendados

### Teste 1: URL Curta
```
URL: Vídeo do YouTube de 2-5 minutos
Palavras: milhão, segredo, importante
Modelo: tiny
Clipes: 3
```

### Teste 2: Pesos Customizados
```
Palavras com pesos:
- "milhão" = 3.0
- "segredo" = 3.0
- "atenção" = 1.0
```

### Teste 3: Arquivo Local
```
Arquivo: Qualquer MP4 local
Palavras: Palavras padrão
Modelo: tiny
```

---

## ✅ Checklist de Funcionalidades

- [ ] Download de URL do YouTube funciona
- [ ] Download de arquivo local funciona
- [ ] Sistema de palavras-chave funciona
- [ ] Pesos são aplicados corretamente
- [ ] Transcrição é exibida nos logs
- [ ] Análise identifica momentos
- [ ] Clipes são gerados
- [ ] Resultados aparecem na aba
- [ ] Botão "Abrir Pasta" funciona
- [ ] Botão "Reproduzir" funciona
- [ ] Barra de progresso atualiza
- [ ] Logs são exibidos em tempo real
- [ ] Erros são tratados adequadamente

---

## 🐛 Troubleshooting

### Erro: "yt_dlp not found"
```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1
```

### Erro: "ffmpeg not found"
```powershell
# Adicionar ao PATH
$env:Path += ";[CAMINHO_DO_FFMPEG]\bin"
```

### GUI não responde
- Verifique a aba "Logs" para mensagens de erro
- O processamento roda em thread separada (não trava a UI)

### Clipes não são gerados
- Verifique se as palavras-chave existem no vídeo
- Tente palavras mais genéricas
- Aumente o número de clipes

---

## 📊 Exemplo de Log Esperado

```
🎬 Iniciando processamento...
📋 Configurações:
   - Palavras-chave: milhão, segredo, importante
   - Modelo: tiny
   - Clipes: 3
   - Modo rápido: Sim
   - Margem de segurança: 8s

📥 ETAPA 1: Download
   URL: https://youtube.com/...
   📹 Título: [Nome do vídeo]
   ⏱️ Duração: 180s (3.0 min)
   ✅ Vídeo: [arquivo].mp4
   ✅ Áudio: [arquivo].wav

🎤 ETAPA 2: Transcrição
   Usando modelo: tiny
   ⚡ Cache ativado
   ✅ 45 segmentos transcritos
   ✅ 2850 caracteres de texto

🔍 ETAPA 3: Análise de Clímax
   🔤 Buscando palavras-chave...
   ✅ 5 momentos semânticos encontrados
   🔊 Analisando picos de volume...
   ✅ 3 picos acústicos encontrados
   ✅ 8 momentos totais identificados
   
   📋 Pontos de Corte:
      1. [45.2s - 75.8s] (30.6s) - keyword: milhão (peso: 2.5)
      2. [120.5s - 155.3s] (34.8s) - keyword: segredo (peso: 3.0)
      3. [200.1s - 245.7s] (45.6s) - keyword: importante (peso: 2.5)

✂️ ETAPA 4: Corte de Vídeo
   📁 Pasta de saída: output_clips_20260102_235430
   🎬 Processando 3 clipes...
   ✅ 3 clipes gerados!

==================================================
📊 RESUMO FINAL
==================================================
Clipes gerados: 3
Pasta de saída: output_clips_20260102_235430

Arquivos:
  1. clip_001.mp4 (5.2 MB)
  2. clip_002.mp4 (6.1 MB)
  3. clip_003.mp4 (7.8 MB)

🎉 Processamento concluído com sucesso!
==================================================
```

---

**Pronto para testar!** 🎬✨
