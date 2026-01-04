"""
Gerenciador de Perfis de Configuração
Branch 03: Flexibilidade via JSON

Permite criar, carregar, salvar e deletar perfis de configuração.
Cada perfil contém: palavras-chave, pesos, configurações de processamento, etc.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ProfileManager:
    """Gerenciador de perfis de configuração"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        """
        Args:
            profiles_dir: Diretório onde os perfis serão salvos
        """
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self.config_file = Path("config.json")
        
    def create_default_profiles(self):
        """Cria perfis padrão se não existirem"""
        
        default_profiles = {
            "Padrão": {
                "name": "Padrão",
                "description": "Configuração padrão balanceada",
                "keywords": [
                    {"keyword": "milhão", "weight": 2.5},
                    {"keyword": "segredo", "weight": 3.0},
                    {"keyword": "importante", "weight": 2.5},
                    {"keyword": "incrível", "weight": 2.0},
                    {"keyword": "atenção", "weight": 1.0}
                ],
                "settings": {
                    "model_size": "tiny",
                    "min_volume_db": -10.0,
                    "cut_duration_min": 30,
                    "cut_duration_max": 90,
                    "max_clips": 5,
                    "safety_margin": 8,
                    "fast_mode": True
                }
            },
            
            "Pablo Marçal": {
                "name": "Pablo Marçal",
                "description": "Otimizado para conteúdo motivacional e polêmico",
                "keywords": [
                    {"keyword": "burro", "weight": 3.0},
                    {"keyword": "dinheiro", "weight": 3.0},
                    {"keyword": "milhão", "weight": 3.0},
                    {"keyword": "prosperar", "weight": 2.5},
                    {"keyword": "lula", "weight": 3.0},
                    {"keyword": "brasil", "weight": 2.5},
                    {"keyword": "sucesso", "weight": 2.5}
                ],
                "settings": {
                    "model_size": "small",
                    "min_volume_db": -12.0,
                    "cut_duration_min": 30,
                    "cut_duration_max": 60,
                    "max_clips": 7,
                    "safety_margin": 10,
                    "fast_mode": True
                }
            },
            
            "Flow Podcast": {
                "name": "Flow Podcast",
                "description": "Para podcasts longos, foco em momentos reflexivos",
                "keywords": [
                    {"keyword": "interessante", "weight": 2.0},
                    {"keyword": "nunca", "weight": 2.5},
                    {"keyword": "sempre", "weight": 2.0},
                    {"keyword": "incrível", "weight": 2.5},
                    {"keyword": "polêmico", "weight": 3.0},
                    {"keyword": "pesado", "weight": 2.5}
                ],
                "settings": {
                    "model_size": "small",
                    "min_volume_db": -15.0,
                    "cut_duration_min": 45,
                    "cut_duration_max": 90,
                    "max_clips": 5,
                    "safety_margin": 8,
                    "fast_mode": True
                }
            },
            
            "Humor": {
                "name": "Humor",
                "description": "Captura momentos engraçados e risadas",
                "keywords": [
                    {"keyword": "kkk", "weight": 3.0},
                    {"keyword": "risada", "weight": 3.0},
                    {"keyword": "engraçado", "weight": 2.5},
                    {"keyword": "hilário", "weight": 2.5},
                    {"keyword": "piada", "weight": 2.0},
                    {"keyword": "meme", "weight": 2.0}
                ],
                "settings": {
                    "model_size": "tiny",
                    "min_volume_db": -8.0,
                    "cut_duration_min": 20,
                    "cut_duration_max": 60,
                    "max_clips": 10,
                    "safety_margin": 5,
                    "fast_mode": True
                }
            }
        }
        
        for profile_name, profile_data in default_profiles.items():
            profile_path = self.profiles_dir / f"{profile_name}.json"
            if not profile_path.exists():
                self.save_profile(profile_name, profile_data)
                logger.info(f"Perfil padrão criado: {profile_name}")
    
    def save_profile(self, name: str, profile_data: Dict) -> bool:
        """
        Salva um perfil
        
        Args:
            name: Nome do perfil
            profile_data: Dados do perfil
            
        Returns:
            True se salvou com sucesso
        """
        try:
            profile_path = self.profiles_dir / f"{name}.json"
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Perfil salvo: {name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar perfil {name}: {e}")
            return False
    
    def load_profile(self, name: str) -> Optional[Dict]:
        """
        Carrega um perfil
        
        Args:
            name: Nome do perfil
            
        Returns:
            Dados do perfil ou None se não existir
        """
        try:
            profile_path = self.profiles_dir / f"{name}.json"
            if not profile_path.exists():
                logger.warning(f"Perfil não encontrado: {name}")
                return None
            
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            logger.info(f"Perfil carregado: {name}")
            return profile_data
        except Exception as e:
            logger.error(f"Erro ao carregar perfil {name}: {e}")
            return None
    
    def delete_profile(self, name: str) -> bool:
        """
        Deleta um perfil
        
        Args:
            name: Nome do perfil
            
        Returns:
            True se deletou com sucesso
        """
        try:
            profile_path = self.profiles_dir / f"{name}.json"
            if profile_path.exists():
                profile_path.unlink()
                logger.info(f"Perfil deletado: {name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao deletar perfil {name}: {e}")
            return False
    
    def list_profiles(self) -> List[str]:
        """
        Lista todos os perfis disponíveis
        
        Returns:
            Lista com nomes dos perfis
        """
        profiles = []
        for profile_path in self.profiles_dir.glob("*.json"):
            profiles.append(profile_path.stem)
        return sorted(profiles)
    
    def export_profile(self, name: str, export_path: str) -> bool:
        """
        Exporta um perfil para outro local
        
        Args:
            name: Nome do perfil
            export_path: Caminho de destino
            
        Returns:
            True se exportou com sucesso
        """
        try:
            profile_data = self.load_profile(name)
            if not profile_data:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Perfil exportado: {name} -> {export_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar perfil {name}: {e}")
            return False
    
    def import_profile(self, import_path: str) -> Optional[str]:
        """
        Importa um perfil de um arquivo
        
        Args:
            import_path: Caminho do arquivo a importar
            
        Returns:
            Nome do perfil importado ou None se falhou
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Validar estrutura mínima
            if 'name' not in profile_data or 'keywords' not in profile_data:
                logger.error("Perfil inválido: faltam campos obrigatórios")
                return None
            
            name = profile_data['name']
            self.save_profile(name, profile_data)
            logger.info(f"Perfil importado: {name}")
            return name
        except Exception as e:
            logger.error(f"Erro ao importar perfil: {e}")
            return None
    
    def save_last_profile(self, profile_name: str):
        """
        Salva o último perfil usado
        
        Args:
            profile_name: Nome do perfil
        """
        try:
            config = {"last_profile": profile_name}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.debug(f"Último perfil salvo: {profile_name}")
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
    
    def get_last_profile(self) -> Optional[str]:
        """
        Obtém o último perfil usado
        
        Returns:
            Nome do último perfil ou None
        """
        try:
            if not self.config_file.exists():
                return None
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get("last_profile")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return None


# Teste do módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    manager = ProfileManager()
    manager.create_default_profiles()
    
    print("\n📋 Perfis disponíveis:")
    for profile in manager.list_profiles():
        print(f"  - {profile}")
    
    print("\n📖 Carregando perfil 'Pablo Marçal':")
    profile = manager.load_profile("Pablo Marçal")
    if profile:
        print(f"  Nome: {profile['name']}")
        print(f"  Descrição: {profile['description']}")
        print(f"  Palavras-chave: {len(profile['keywords'])}")
