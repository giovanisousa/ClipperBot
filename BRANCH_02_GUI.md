# 🎨 Branch 02 - Interface Gráfica (GUI)

## 📋 Visão Geral

Interface gráfica moderna e intuitiva para o ClipperBot usando **CustomTkinter**.

## ✨ Recursos Implementados

### 🎯 Funcionalidades Principais
- ✅ Interface moderna em tema dark
- ✅ Entrada via URL do YouTube ou arquivo local
- ✅ Sistema visual de gerenciamento de palavras-chave com pesos
- ✅ Configurações avançadas (modelo, número de clipes, margem de segurança)
- ✅ Sistema de tabs (Status, Resultados, Logs)
- ✅ Barra de progresso em tempo real
- ✅ Modo rápido configurável

### 🎨 Layout
```
┌──────────────┬────────────────────────┐
│              │   📊 Status            │
│   Sidebar    │   🎬 Resultados        │
│  (Config)    │   📝 Logs              │
│              │                        │
│  • Entrada   │   [Área de conteúdo]  │
│  • Keywords  │                        │
│  • Settings  │                        │
│  • [Botão]   │                        │
└──────────────┴────────────────────────┘
```

## 🚀 Como Usar

### Instalar dependências:
```powershell
.\.venv\Scripts\Activate.ps1
pip install customtkinter Pillow
```

### Executar GUI:
```powershell
python gui_main.py
```

## 📖 Guia de Uso

### 1. Entrada de Vídeo
- **URL do YouTube**: Cole o link do vídeo
- **Arquivo Local**: Selecione um arquivo MP4/AVI/MKV

### 2. Palavras-Chave
- Digite a palavra-chave
- Ajuste o peso (1.0 a 3.0)
- Clique em ➕ para adicionar
- Use "📋 Padrão" para carregar palavras sugeridas

### 3. Configurações
- **Modelo**: tiny (rápido) até medium (preciso)
- **Número de Clipes**: 1 a 10
- **Modo Rápido**: Ativa cache e otimizações
- **Margem de Segurança**: 5 a 15 segundos

### 4. Processar
- Clique em "🚀 Processar Vídeo"
- Acompanhe o progresso na aba Status
- Veja os resultados na aba Resultados

## 🎨 Capturas de Tela

### Tela Principal
Interface moderna com tema dark, sidebar de configurações e área de visualização com tabs.

### Sistema de Palavras-Chave
Gerenciamento visual de palavras com controle de peso via slider.

### Status e Progresso
Feedback em tempo real do processamento com barra de progresso e logs detalhados.

## 🔧 Estrutura do Código

```
gui_main.py
├── ClipperBotGUI (classe principal)
│   ├── _create_sidebar()          # Barra lateral de configurações
│   │   ├── _create_video_input_section()
│   │   ├── _create_keywords_section()
│   │   └── _create_advanced_settings()
│   ├── _create_main_area()        # Área principal com tabs
│   │   ├── _create_preview_tab()  # Status e progresso
│   │   ├── _create_results_tab()  # Lista de clipes
│   │   └── _create_logs_tab()     # Logs detalhados
│   └── Event Handlers
│       ├── start_processing()     # Inicia processamento
│       ├── process_video()        # Thread de processamento
│       └── ...
```

## 📝 Próximos Passos

### Em Desenvolvimento
- [ ] Integração com o backend (core engine)
- [ ] Preview de vídeo inline
- [ ] Player de clipes integrado
- [ ] Exportação de configurações
- [ ] Histórico de processamentos
- [ ] Drag & drop de arquivos
- [ ] Temas customizáveis

### Futuras Melhorias
- [ ] Edição visual de clipes
- [ ] Timeline interativa
- [ ] Estatísticas de uso
- [ ] Perfis de configuração salvos

## 🎯 Design System

### Cores
- **Background**: #2b2b2b
- **Primary**: #1f538d (azul)
- **Success**: #28a745 (verde)
- **Danger**: #dc3545 (vermelho)
- **Text**: white / gray

### Tipografia
- **Títulos**: CTkFont(size=24, weight="bold")
- **Subtítulos**: CTkFont(size=14, weight="bold")
- **Corpo**: CTkFont(size=12)
- **Logs**: Consolas, size=10

### Componentes
- **CTkButton**: Altura 50px para ações principais
- **CTkEntry**: Altura 35px
- **CTkSlider**: Controles de valores numéricos
- **CTkSwitch**: Toggles on/off
- **CTkOptionMenu**: Dropdowns de seleção

## 🐛 Troubleshooting

### GUI não abre
```powershell
# Reinstalar CustomTkinter
pip install --upgrade customtkinter
```

### Erro de tema
```python
# Verificar modo de aparência
ctk.set_appearance_mode("dark")  # ou "light"
```

### Performance lenta
- Ative o "Modo Rápido" nas configurações
- Use modelo "tiny" para testes
- Reduza o número de clipes

## 📚 Recursos

- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)

---

**Status**: 🚧 Em Desenvolvimento  
**Versão**: 1.0.0-beta  
**Última Atualização**: 02/01/2026
