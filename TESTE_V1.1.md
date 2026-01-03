# ⚡ Comando de Teste - ClipperBot v1.1

## 🎯 Teste Rápido das Melhorias

### Ative o ambiente virtual primeiro:
```powershell
.\.venv\Scripts\Activate.ps1
$env:Path += ";C:\Users\Giovani Souza\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
```

### Comando de Teste (mesmo vídeo anterior):
```powershell
python main_cli.py `
  --url "https://www.youtube.com/watch?v=c22SGNvj3GM" `
  --fast `
  --model tiny `
  --keywords "milhão,segredo,atenção,incrível,importante,prosperar" `
  --max-clips 5 `
  --min-duration 30 `
  --max-duration 90 `
  --output ./meus_cortes_v11
```

### Com Pesos Customizados:
```powershell
python main_cli.py `
  --url "https://www.youtube.com/watch?v=c22SGNvj3GM" `
  --fast `
  --model tiny `
  --keywords "milhão,segredo,lula,atenção,importante,prosperar" `
  --weights-config examples/custom_weights.json `
  --max-clips 5 `
  --min-duration 30 `
  --max-duration 90 `
  --output ./meus_cortes_v11
```

### Ajustando Margem de Segurança:
```powershell
# Mais contexto no final (10 segundos)
python main_cli.py `
  --url "https://www.youtube.com/watch?v=c22SGNvj3GM" `
  --fast `
  --model tiny `
  --keywords "milhão,segredo,lula" `
  --safety-margin 10 `
  --max-clips 5 `
  --output ./meus_cortes_v11
```

---

## 🔍 O Que Observar nos Resultados

### Melhorias Implementadas:

1. **Frases Completas**
   - ✅ Nenhum vídeo deve terminar em vírgula
   - ✅ Todos devem terminar em ponto final/interrogação
   - ✅ Contexto completo da frase

2. **Priorização Inteligente**
   - ✅ Clipes com "lula", "segredo", "milhão" devem aparecer primeiro
   - ✅ Clipes com "atenção" devem aparecer depois (menor prioridade)

3. **Margem de Segurança**
   - ✅ +8 segundos automáticos no final
   - ✅ Sem cortes abruptos
   - ✅ Melhor para edição final

---

## 📊 Comparação com v1.0

Execute os dois comandos para comparar:

### v1.0 (output antigo):
```powershell
# Se ainda existir: ./meus_cortes/
```

### v1.1 (output novo):
```powershell
# Novo output: ./meus_cortes_v11/
```

### Checklist de Qualidade:
- [ ] Frases completas (não cortadas)
- [ ] Melhores palavras-chave primeiro
- [ ] Final com margem adequada
- [ ] Nenhum corte em vírgula

---

## 🎬 Vídeos Esperados (Ordem de Prioridade)

Com base nos pesos implementados:

| Ordem | Palavra-chave | Peso | Qualidade |
|-------|---------------|------|-----------|
| 1º | "lula" | 3.0 | ⭐⭐⭐ Excelente |
| 2º | "segredo" | 3.0 | ⭐⭐⭐ Excelente |
| 3º | "milhão" | 2.5 | ⭐⭐ Muito Bom |
| 4º | "importante" | 2.5 | ⭐⭐ Muito Bom |
| 5º | "prosperar" | 2.0 | ⭐ Bom |

---

## 🐛 Troubleshooting

### Erro: "yt_dlp not found"
```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1
```

### Erro: "ffmpeg not found"
```powershell
# Adicionar FFmpeg ao PATH
$env:Path += ";C:\Users\Giovani Souza\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
```

### Verificar se está tudo OK:
```powershell
python --version
ffmpeg -version
pip list | Select-String "yt-dlp"
```

---

**Pronto para testar!** 🚀
