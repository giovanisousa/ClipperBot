"""
Hardware ID Generator
Branch 04: Sistema de Segurança e Licenciamento

Gera um identificador único e consistente da máquina para Hardware Lock.
Combina CPU Serial + Motherboard Serial para criar uma "impressão digital" imutável.
"""

import hashlib
import platform
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class HardwareIDGenerator:
    """Gerador de Hardware ID único por máquina"""
    
    @staticmethod
    def _get_windows_hwid() -> Optional[str]:
        """
        Obtém HWID no Windows usando WMIC
        
        Returns:
            String única da máquina ou None se falhar
        """
        try:
            # CPU ID
            cpu_command = 'wmic cpu get ProcessorId'
            cpu_output = subprocess.check_output(cpu_command, shell=True).decode()
            cpu_id = ''.join(cpu_output.split('\n')[1:]).strip()
            
            # Motherboard Serial
            mb_command = 'wmic baseboard get SerialNumber'
            mb_output = subprocess.check_output(mb_command, shell=True).decode()
            mb_serial = ''.join(mb_output.split('\n')[1:]).strip()
            
            # Disk Serial (mais um elemento de segurança)
            disk_command = 'wmic diskdrive get SerialNumber'
            disk_output = subprocess.check_output(disk_command, shell=True).decode()
            disk_serial = ''.join(disk_output.split('\n')[1:]).strip()
            
            # Combinar todos
            combined = f"{cpu_id}-{mb_serial}-{disk_serial}"
            
            logger.debug(f"Windows HWID components: CPU={cpu_id}, MB={mb_serial}, DISK={disk_serial}")
            return combined
            
        except Exception as e:
            logger.error(f"Erro ao obter HWID Windows: {e}")
            return None
    
    @staticmethod
    def _get_linux_hwid() -> Optional[str]:
        """
        Obtém HWID no Linux
        
        Returns:
            String única da máquina ou None se falhar
        """
        try:
            # Machine ID (mais confiável no Linux)
            with open('/etc/machine-id', 'r') as f:
                machine_id = f.read().strip()
            
            # CPU Info
            cpu_command = "cat /proc/cpuinfo | grep 'Serial' | awk '{print $3}'"
            cpu_output = subprocess.check_output(cpu_command, shell=True).decode().strip()
            
            # Combinar
            combined = f"{machine_id}-{cpu_output}" if cpu_output else machine_id
            
            logger.debug(f"Linux HWID: {combined}")
            return combined
            
        except Exception as e:
            logger.error(f"Erro ao obter HWID Linux: {e}")
            return None
    
    @staticmethod
    def _get_mac_hwid() -> Optional[str]:
        """
        Obtém HWID no macOS
        
        Returns:
            String única da máquina ou None se falhar
        """
        try:
            # Hardware UUID
            command = "system_profiler SPHardwareDataType | grep 'Hardware UUID'"
            output = subprocess.check_output(command, shell=True).decode()
            uuid = output.split(':')[1].strip()
            
            logger.debug(f"macOS HWID: {uuid}")
            return uuid
            
        except Exception as e:
            logger.error(f"Erro ao obter HWID macOS: {e}")
            return None
    
    @classmethod
    def generate_hwid(cls) -> str:
        """
        Gera um Hardware ID único e consistente para a máquina atual
        
        Returns:
            Hash MD5 do HWID (32 caracteres)
        """
        system = platform.system()
        
        logger.info(f"Gerando HWID para sistema: {system}")
        
        # Obter informações específicas do SO
        if system == "Windows":
            raw_hwid = cls._get_windows_hwid()
        elif system == "Linux":
            raw_hwid = cls._get_linux_hwid()
        elif system == "Darwin":  # macOS
            raw_hwid = cls._get_mac_hwid()
        else:
            logger.error(f"Sistema operacional não suportado: {system}")
            raw_hwid = None
        
        # Fallback: usar hostname + username (menos seguro)
        if not raw_hwid:
            logger.warning("Usando fallback para HWID (menos seguro)")
            import socket
            import getpass
            raw_hwid = f"{socket.gethostname()}-{getpass.getuser()}-{platform.node()}"
        
        # Criar hash MD5 (fixo em 32 caracteres)
        hwid_hash = hashlib.md5(raw_hwid.encode()).hexdigest()
        
        logger.info(f"HWID gerado: {hwid_hash}")
        return hwid_hash
    
    @classmethod
    def verify_hwid(cls, stored_hwid: str) -> bool:
        """
        Verifica se o HWID atual corresponde ao armazenado
        
        Args:
            stored_hwid: HWID armazenado para comparação
            
        Returns:
            True se corresponde, False caso contrário
        """
        current_hwid = cls.generate_hwid()
        matches = current_hwid == stored_hwid
        
        if matches:
            logger.info("✅ HWID verificado com sucesso")
        else:
            logger.warning(f"❌ HWID não corresponde: atual={current_hwid}, esperado={stored_hwid}")
        
        return matches


# Teste do módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🔐 Testando Gerador de Hardware ID\n")
    
    # Gerar HWID
    hwid = HardwareIDGenerator.generate_hwid()
    print(f"Hardware ID: {hwid}")
    print(f"Tamanho: {len(hwid)} caracteres")
    
    # Testar consistência (deve ser o mesmo)
    hwid2 = HardwareIDGenerator.generate_hwid()
    print(f"\nSegunda geração: {hwid2}")
    print(f"Consistente: {'✅ SIM' if hwid == hwid2 else '❌ NÃO'}")
    
    # Testar verificação
    print(f"\nVerificação: {'✅ PASSOU' if HardwareIDGenerator.verify_hwid(hwid) else '❌ FALHOU'}")
