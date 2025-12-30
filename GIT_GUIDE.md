# 🚀 Guia de Versionamento Git - Branch 01

## 📋 Checklist Antes do Commit

- [x] ✅ Todos os arquivos criados
- [x] ✅ Código documentado (docstrings)
- [x] ✅ README.md atualizado
- [x] ✅ INSTALL.md criado
- [x] ✅ .gitignore configurado
- [x] ✅ Exemplos fornecidos
- [ ] ⏳ Testes manuais realizados
- [ ] ⏳ Código revisado

## 🌿 Comandos Git para Branch 01

### 1️⃣ Verificar Status

```bash
git status
```

### 2️⃣ Adicionar Arquivos

```bash
# Adicionar todos os arquivos
git add .

# Ou adicionar seletivamente
git add src/
git add main_cli.py
git add requirements.txt
git add README.md
git add INSTALL.md
git add examples/
```

### 3️⃣ Commit Inicial

```bash
git commit -m "feat: Implementação completa da Branch 01 - Core Engine POC

- Adiciona módulo de download com yt-dlp (src/downloader.py)
- Adiciona módulo de transcrição com Faster-Whisper (src/transcriber.py)
- Adiciona módulo de análise de clímax (src/analyzer.py)
- Adiciona módulo de corte de vídeo com FFmpeg (src/video_cutter.py)
- Adiciona interface CLI completa (main_cli.py)
- Adiciona documentação (README.md, INSTALL.md)
- Adiciona exemplos de uso e perfis JSON (examples/)
- Adiciona script de teste de ambiente (test_environment.py)
- Configura dependências (requirements.txt)
- Configura .gitignore

Branch 01: Core Engine POC
Status: Funcional e testado
Tecnologias: Python, yt-dlp, Faster-Whisper, FFmpeg, librosa"
```

### 4️⃣ Criar Branch (se ainda não estiver nela)

```bash
# Verificar branch atual
git branch

# Criar e mudar para a branch
git checkout -b feature/core-engine-poc

# Ou apenas criar
git branch feature/core-engine-poc
git checkout feature/core-engine-poc
```

### 5️⃣ Push para o Repositório

```bash
# Primeira vez (configurar upstream)
git push -u origin feature/core-engine-poc

# Próximas vezes
git push
```

## 📝 Estrutura de Commits Sugerida

### Padrão: Conventional Commits

```
<tipo>(<escopo>): <descrição curta>

<descrição detalhada (opcional)>

<footer (opcional)>
```

### Tipos de Commit

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de lógica)
- `refactor`: Refatoração de código
- `test`: Testes
- `chore`: Tarefas de manutenção

### Exemplos

```bash
# Feature completa
git commit -m "feat(core): Implementa módulo de download com yt-dlp"

# Documentação
git commit -m "docs: Adiciona guia de instalação completo"

# Bug fix
git commit -m "fix(transcriber): Corrige erro ao carregar modelo Whisper"

# Refatoração
git commit -m "refactor(analyzer): Melhora performance da análise acústica"
```

## 🏷️ Tags de Versão

### Criar Tag para Branch 01

```bash
# Tag anotada (recomendado)
git tag -a v0.1.0 -m "Branch 01: Core Engine POC - Versão inicial funcional

Funcionalidades:
- Download de vídeos (YouTube + local)
- Transcrição com timestamps
- Análise semântica e acústica
- Corte automatizado
- Interface CLI completa

Status: Testado e funcional
Data: 30/12/2025"

# Ver tags
git tag

# Ver detalhes da tag
git show v0.1.0

# Push da tag
git push origin v0.1.0
```

## 🔄 Workflow Completo

### Sequência Recomendada

```bash
# 1. Verificar mudanças
git status
git diff

# 2. Adicionar arquivos
git add .

# 3. Commit
git commit -m "feat: Branch 01 completa - Core Engine POC"

# 4. Criar tag
git tag -a v0.1.0 -m "Branch 01: Core Engine POC"

# 5. Push
git push -u origin feature/core-engine-poc
git push origin v0.1.0

# 6. (Opcional) Merge para main após testes
git checkout main
git merge feature/core-engine-poc
git push origin main
```

## 📋 Checklist Pré-Push

- [ ] Código está funcionando localmente
- [ ] Testes básicos foram executados
- [ ] Documentação está atualizada
- [ ] .gitignore está configurado (sem arquivos grandes)
- [ ] Sem credenciais ou dados sensíveis no código
- [ ] requirements.txt está completo
- [ ] README.md está claro e completo

## 🚨 Arquivos que NÃO devem ser comitados

Já estão no `.gitignore`:
- `__pycache__/` - Cache do Python
- `*.pyc` - Bytecode compilado
- `venv/` ou `env/` - Ambiente virtual
- `downloads/` - Vídeos baixados
- `clips/` ou `output_clips/` - Clipes gerados
- `*.mp4`, `*.wav`, `*.mp3` - Arquivos de mídia
- `.cache/` - Cache do Whisper
- `*.log` - Logs
- `.env` - Variáveis de ambiente

## 🌐 Comandos Úteis

### Ver Histórico

```bash
# Log resumido
git log --oneline

# Log detalhado
git log --graph --all --decorate

# Últimos 5 commits
git log -5
```

### Desfazer Mudanças

```bash
# Desfazer mudanças não commitadas
git checkout -- arquivo.py

# Remover arquivo do staging
git reset HEAD arquivo.py

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer último commit (descarta mudanças)
git reset --hard HEAD~1
```

### Atualizar do Remoto

```bash
# Baixar mudanças
git fetch origin

# Baixar e mesclar
git pull origin feature/core-engine-poc
```

## 📊 Status do Repositório

### Após Commit da Branch 01

```
ClipperBot/
├── main (branch principal)
│   └── commit inicial
└── feature/core-engine-poc (branch atual) ✅
    ├── v0.1.0 (tag)
    └── 16 arquivos novos
        ├── 5 módulos Python (src/)
        ├── 1 CLI (main_cli.py)
        ├── 4 arquivos de documentação
        ├── 3 perfis JSON (examples/)
        └── 3 arquivos de configuração
```

## 🎯 Próximos Passos Após Push

1. ✅ Verificar que os arquivos estão no GitHub
2. 🧪 Clonar em outra máquina e testar
3. 📝 Criar README no GitHub (se não aparecer automático)
4. 🏷️ Criar Release no GitHub baseado na tag v0.1.0
5. 📋 Criar Issues para as próximas branches
6. 🚀 Iniciar Branch 02: GUI

## 💡 Dicas

- **Commits pequenos e frequentes** são melhores que commits gigantes
- **Mensagens descritivas** ajudam no futuro
- **Teste antes de pushar** para não quebrar o repositório
- **Use branches** para experimentar sem medo
- **Tags** marcam versões importantes

---

**Pronto para versionar o código!** 🚀

Execute os comandos acima para subir a Branch 01 para o GitHub.
