"""
Authentication Client
Branch 04: Sistema de Segurança e Licenciamento

Cliente responsável por comunicação com API de autenticação,
gerenciamento de JWT tokens e validação de sessão.
"""

import requests
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Exceção para erros de autenticação"""
    pass


class AuthClient:
    """Cliente de autenticação com API"""
    
    # Configuração da API
    # PRODUÇÃO: Alterar para URL do Render após deploy
    # Exemplo: https://clipperbot-auth-api.onrender.com/api
    API_BASE_URL = "http://localhost:8000/api"  # Local para desenvolvimento
    TOKEN_FILE = Path.home() / ".clipperbot" / "session.json"
    
    def __init__(self):
        """Inicializa cliente de autenticação"""
        self.token: Optional[str] = None
        self.user_data: Optional[Dict[str, Any]] = None
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Garante que diretório de configuração existe"""
        self.TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    def login(self, email: str, password: str, hwid: str) -> Dict[str, Any]:
        """
        Realiza login na API
        
        Args:
            email: Email do usuário
            password: Senha
            hwid: Hardware ID da máquina
            
        Returns:
            Dados do usuário e token JWT
            
        Raises:
            AuthenticationError: Se login falhar
        """
        try:
            logger.info(f"Tentando login para {email}")
            
            response = requests.post(
                f"{self.API_BASE_URL}/auth/login",
                json={
                    "email": email,
                    "password": password,
                    "hwid": hwid
                },
                timeout=10
            )
            
            # Tratamento de erros específicos
            if response.status_code == 401:
                raise AuthenticationError("❌ Email ou senha inválidos")
            
            elif response.status_code == 403:
                data = response.json()
                if "expired" in data.get("detail", "").lower():
                    raise AuthenticationError("❌ Sua assinatura expirou. Renove em https://seu-site.com")
                elif "inactive" in data.get("detail", "").lower():
                    raise AuthenticationError("❌ Conta inativa. Entre em contato com suporte.")
                else:
                    raise AuthenticationError("❌ Acesso negado")
            
            elif response.status_code == 409:
                raise AuthenticationError(
                    "❌ Esta licença já está em uso em outro computador.\n"
                    "Você tem 2 opções:\n"
                    "1. Liberar a licença no outro PC (Config > Liberar Licença)\n"
                    "2. Usar o Reset disponível mensalmente"
                )
            
            elif response.status_code != 200:
                logger.error(f"Erro HTTP {response.status_code}: {response.text}")
                raise AuthenticationError(f"❌ Erro ao fazer login: {response.status_code}")
            
            # Sucesso
            data = response.json()
            self.token = data.get("access_token")
            self.user_data = data.get("user")
            
            # Salvar sessão
            self._save_session(data)
            
            logger.info(f"✅ Login realizado com sucesso: {email}")
            return data
            
        except requests.exceptions.ConnectionError:
            logger.error("Falha ao conectar com servidor de autenticação")
            raise AuthenticationError(
                "❌ Não foi possível conectar ao servidor.\n"
                "Verifique sua conexão com a internet."
            )
        
        except requests.exceptions.Timeout:
            logger.error("Timeout ao conectar com servidor")
            raise AuthenticationError("❌ Timeout: Servidor não respondeu")
        
        except AuthenticationError:
            raise
        
        except Exception as e:
            logger.exception("Erro inesperado no login")
            raise AuthenticationError(f"❌ Erro inesperado: {str(e)}")
    
    def validate_session(self) -> bool:
        """
        Valida sessão atual (verifica token JWT)
        
        Returns:
            True se sessão válida, False caso contrário
        """
        try:
            # Tentar carregar sessão salva
            if not self.token:
                session_data = self._load_session()
                if not session_data:
                    logger.info("Nenhuma sessão encontrada")
                    return False
                
                self.token = session_data.get("access_token")
                self.user_data = session_data.get("user")
            
            # Validar com API
            response = requests.get(
                f"{self.API_BASE_URL}/auth/validate",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Sessão válida")
                return True
            else:
                logger.warning(f"Sessão inválida: {response.status_code}")
                self._clear_session()
                return False
                
        except Exception as e:
            logger.error(f"Erro ao validar sessão: {e}")
            return False
    
    def logout(self):
        """Faz logout e limpa sessão"""
        try:
            if self.token:
                # Notificar API (opcional)
                requests.post(
                    f"{self.API_BASE_URL}/auth/logout",
                    headers={"Authorization": f"Bearer {self.token}"},
                    timeout=5
                )
        except:
            pass
        finally:
            self._clear_session()
            logger.info("Logout realizado")
    
    def release_license(self, email: str, password: str) -> bool:
        """
        Libera licença do HWID atual (permite usar em outro PC)
        
        Args:
            email: Email do usuário
            password: Senha para confirmação
            
        Returns:
            True se liberado com sucesso
        """
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/auth/release",
                json={"email": email, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Licença liberada com sucesso")
                self._clear_session()
                return True
            else:
                logger.error(f"Erro ao liberar licença: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao liberar licença: {e}")
            return False
    
    def _save_session(self, data: Dict[str, Any]):
        """Salva sessão em arquivo local"""
        try:
            session_data = {
                "access_token": data.get("access_token"),
                "user": data.get("user"),
                "saved_at": datetime.now().isoformat()
            }
            
            with open(self.TOKEN_FILE, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.debug(f"Sessão salva em {self.TOKEN_FILE}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar sessão: {e}")
    
    def _load_session(self) -> Optional[Dict[str, Any]]:
        """Carrega sessão salva"""
        try:
            if not self.TOKEN_FILE.exists():
                return None
            
            with open(self.TOKEN_FILE, 'r') as f:
                data = json.load(f)
            
            # Verificar se não expirou (sessão válida por 7 dias)
            saved_at = datetime.fromisoformat(data.get("saved_at"))
            if datetime.now() - saved_at > timedelta(days=7):
                logger.info("Sessão expirada")
                self._clear_session()
                return None
            
            logger.debug("Sessão carregada do arquivo")
            return data
            
        except Exception as e:
            logger.error(f"Erro ao carregar sessão: {e}")
            return None
    
    def _clear_session(self):
        """Limpa sessão"""
        self.token = None
        self.user_data = None
        
        try:
            if self.TOKEN_FILE.exists():
                self.TOKEN_FILE.unlink()
                logger.debug("Arquivo de sessão removido")
        except Exception as e:
            logger.error(f"Erro ao remover arquivo de sessão: {e}")
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Retorna informações do usuário logado
        
        Returns:
            Dicionário com dados do usuário ou None
        """
        return self.user_data
    
    def is_authenticated(self) -> bool:
        """Verifica se usuário está autenticado"""
        return self.token is not None and self.user_data is not None


# Teste do módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🔐 Testando Cliente de Autenticação\n")
    
    client = AuthClient()
    print(f"API Base URL: {client.API_BASE_URL}")
    print(f"Token File: {client.TOKEN_FILE}")
    print(f"Autenticado: {client.is_authenticated()}")
