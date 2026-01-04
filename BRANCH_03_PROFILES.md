# 🌿 Branch 03 - Sistema de Perfis JSON

## 📋 Visão Geral

Sistema completo de gerenciamento de perfis configuráveis via JSON. Permite criar, salvar, carregar e compartilhar perfis de configuração sem mexer no código.

## ✨ Funcionalidades Implementadas

### 🎯 Gerenciamento de Perfis
- ✅ Criar novos perfis
- ✅ Salvar/Atualizar perfis existentes
- ✅ Carregar perfis
- ✅ Importar perfis de arquivos JSON
- ✅ Exportar perfis para compartilhamento
- ✅ Deletar perfis
- ✅ Listar todos os perfis disponíveis

### 💾 Persistência
- ✅ Salva automaticamente o último perfil usado
- ✅ Carrega automaticamente na próxima execução
- ✅ Armazena perfis em arquivos JSON
- ✅ Estrutura de pastas organizada

### 👥 Perfis Padrão Incluídos

#### 1. **Padrão**
Configuração balanceada para uso geral
- Palavras: milhão (2.5), segredo (3.0), importante (2.5), incrível (2.0), atenção (1.0)
- Modelo: tiny
- Clipes: 5
- Duração: 30-90s

#### 2. **Pablo Marçal**
Otimizado para conteúdo motivacional e polêmico
- Palavras: burro (3.0), dinheiro (3.0), milhão (3.0), prosperar (2.5), lula (3.0), brasil (2.5), sucesso (2.5)
- Modelo: small
- Clipes: 7
- Duração: 30-60s
- Margem: 10s

#### 3. **Flow Podcast**
Para podcasts longos, foco em momentos reflexivos
- Palavras: interessante (2.0), nunca (2.5), sempre (2.0), incrível (2.5), polêmico (3.0), pesado (2.5)
- Modelo: small
- Clipes: 5
- Duração: 45-90s

#### 4. **Humor**
Captura momentos engraçados e risadas
- Palavras: kkk (3.0), risada (3.0), engraçado (2.5), hilário (2.5), piada (2.0), meme (2.0)
- Modelo: tiny
- Clipes: 10
- Duração: 20-60s
- Margem: 5s

## 🏗️ Estrutura de Arquivos

```
ClipperBot/
├── profiles/                    # Pasta de perfis
│   ├── Padrão.json
│   ├── Pablo Marçal.json
│   ├── Flow Podcast.json
│   ├── Humor.json
│   └── [seus perfis].json
├── config.json                  # Configuração global (último perfil)
└── src/
    └── profile_manager.py      # Módulo de gerenciamento
```

## 📄 Formato do Perfil JSON

```json
{
  "name": "Meu Perfil",
  "description": "Descrição do perfil",
  "keywords": [
    {"keyword": "palavra1", "weight": 3.0},
    {"keyword": "palavra2", "weight": 2.5},
    {"keyword": "palavra3", "weight": 2.0}
  ],
  "settings": {
    "model_size": "tiny",
    "min_volume_db": -10.0,
    "cut_duration_min": 30,
    "cut_duration_max": 90,
    "max_clips": 5,
    "safety_margin": 8,
    "fast_mode": true
  }
}
```

## 🚀 Como Usar

### Na Interface Gráfica

#### 1. **Selecionar Perfil**
- Use o dropdown "👤 Perfil de Configuração"
- Escolha um dos perfis disponíveis
- As configurações serão carregadas automaticamente

#### 2. **Criar Novo Perfil**
1. Configure palavras-chave e ajustes
2. Clique em "➕ Novo"
3. Digite o nome do perfil
4. Pronto! Perfil criado

#### 3. **Salvar Alterações**
1. Faça alterações nas configurações
2. Clique em "💾 Salvar"
3. Confirme a sobrescrita

#### 4. **Exportar Perfil**
1. Selecione o perfil
2. Clique em "📤 Exportar"
3. Escolha local para salvar
4. Compartilhe o arquivo JSON

#### 5. **Importar Perfil**
1. Clique em "📂 Importar"
2. Selecione o arquivo JSON
3. Perfil adicionado à lista

### Via Código Python

```python
from src.profile_manager import ProfileManager

# Inicializar gerenciador
manager = ProfileManager()

# Listar perfis
profiles = manager.list_profiles()
print(profiles)  # ['Padrão', 'Pablo Marçal', 'Flow Podcast', 'Humor']

# Carregar perfil
profile = manager.load_profile("Pablo Marçal")
print(profile['keywords'])

# Criar novo perfil
new_profile = {
    "name": "Meu Perfil",
    "description": "Perfil customizado",
    "keywords": [
        {"keyword": "teste", "weight": 3.0}
    ],
    "settings": {
        "model_size": "tiny",
        "max_clips": 5,
        "fast_mode": True
    }
}
manager.save_profile("Meu Perfil", new_profile)

# Exportar
manager.export_profile("Meu Perfil", "meu_perfil.json")

# Importar
manager.import_profile("perfil_compartilhado.json")
```

## 🎯 Casos de Uso

### Caso 1: Podcast de Humor
```json
{
  "name": "Podcast Humor",
  "keywords": [
    {"keyword": "risada", "weight": 3.0},
    {"keyword": "kkk", "weight": 3.0},
    {"keyword": "hilário", "weight": 2.5}
  ],
  "settings": {
    "model_size": "tiny",
    "max_clips": 10,
    "cut_duration_min": 20,
    "cut_duration_max": 60,
    "safety_margin": 5
  }
}
```

### Caso 2: Conteúdo Educacional
```json
{
  "name": "Educacional",
  "keywords": [
    {"keyword": "importante", "weight": 3.0},
    {"keyword": "atenção", "weight": 2.5},
    {"keyword": "lembre-se", "weight": 2.5},
    {"keyword": "fundamental", "weight": 3.0}
  ],
  "settings": {
    "model_size": "small",
    "max_clips": 5,
    "cut_duration_min": 45,
    "cut_duration_max": 90
  }
}
```

### Caso 3: Conteúdo Viral
```json
{
  "name": "Viral",
  "keywords": [
    {"keyword": "polêmico", "weight": 3.0},
    {"keyword": "chocante", "weight": 3.0},
    {"keyword": "absurdo", "weight": 2.5},
    {"keyword": "inacreditável", "weight": 2.5}
  ],
  "settings": {
    "model_size": "tiny",
    "max_clips": 8,
    "cut_duration_min": 15,
    "cut_duration_max": 45,
    "safety_margin": 5
  }
}
```

## 🔧 API do ProfileManager

### Métodos Principais

```python
class ProfileManager:
    def save_profile(name: str, profile_data: Dict) -> bool
    def load_profile(name: str) -> Optional[Dict]
    def delete_profile(name: str) -> bool
    def list_profiles() -> List[str]
    def export_profile(name: str, export_path: str) -> bool
    def import_profile(import_path: str) -> Optional[str]
    def save_last_profile(profile_name: str)
    def get_last_profile() -> Optional[str]
    def create_default_profiles()
```

## 📊 Benefícios

### Para Usuários
- ✅ **Sem código**: Configure tudo pela interface
- ✅ **Reutilizável**: Salve configurações favoritas
- ✅ **Compartilhável**: Exporte e compartilhe perfis
- ✅ **Flexível**: Adapte para cada tipo de conteúdo
- ✅ **Persistente**: Lembra suas preferências

### Para Desenvolvedores
- ✅ **Modular**: Código separado em módulo próprio
- ✅ **Testável**: Fácil de testar isoladamente
- ✅ **Extensível**: Fácil adicionar novos campos
- ✅ **Documentado**: Código bem comentado
- ✅ **Type hints**: Melhor suporte IDE

## 🧪 Testes

### Testar Perfis
```powershell
# Testar módulo
python src/profile_manager.py

# Testar GUI
python gui_main.py
```

### Workflow de Teste
1. Criar novo perfil "Teste"
2. Adicionar palavras-chave
3. Salvar perfil
4. Fechar aplicação
5. Reabrir aplicação
6. Verificar se perfil "Teste" persiste
7. Exportar perfil
8. Deletar perfil
9. Importar perfil exportado

## 🚀 Próximos Passos

### Melhorias Futuras
- [ ] Duplicar perfis
- [ ] Renomear perfis
- [ ] Validação avançada de perfis
- [ ] Templates de perfis online
- [ ] Backup automático de perfis
- [ ] Histórico de modificações

---

**Status**: ✅ Completo  
**Versão**: 1.0.0  
**Data**: 04/01/2026
