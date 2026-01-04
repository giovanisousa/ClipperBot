"""
Login Screen
Branch 04: Sistema de Segurança e Licenciamento

Tela de login que bloqueia acesso à aplicação principal.
Valida credenciais, hardware ID e status da assinatura.
"""

import customtkinter as ctk
from tkinter import messagebox
import logging
import threading
from typing import Optional, Dict, Any

from src.hwid_generator import HardwareIDGenerator
from src.auth_client import AuthClient, AuthenticationError

logger = logging.getLogger(__name__)


class LoginWindow(ctk.CTk):
    """Janela de login do ClipperBot"""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("ClipperBot - Login")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Centralizar janela
        self._center_window()
        
        # Estado
        self.auth_client = AuthClient()
        self.hwid = HardwareIDGenerator.generate_hwid()
        self.authenticated = False
        self.user_data: Optional[Dict[str, Any]] = None
        
        # Criar interface
        self._create_widgets()
        
        # Tentar login automático
        self.after(500, self._try_auto_login)
        
        logger.info("Janela de login inicializada")
    
    def _center_window(self):
        """Centraliza janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Cria elementos da interface"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎬 ClipperBot",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Sistema de Cortes Inteligentes",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Card de login
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(fill="both", expand=True)
        
        # Título do card
        card_title = ctk.CTkLabel(
            login_frame,
            text="Fazer Login",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        card_title.pack(pady=(30, 20))
        
        # Campo Email
        email_label = ctk.CTkLabel(login_frame, text="Email:", anchor="w")
        email_label.pack(pady=(10, 5), padx=30, fill="x")
        
        self.email_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="seu@email.com",
            height=40
        )
        self.email_entry.pack(pady=(0, 15), padx=30, fill="x")
        
        # Campo Senha
        password_label = ctk.CTkLabel(login_frame, text="Senha:", anchor="w")
        password_label.pack(pady=(0, 5), padx=30, fill="x")
        
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="••••••••",
            show="•",
            height=40
        )
        self.password_entry.pack(pady=(0, 20), padx=30, fill="x")
        
        # Botão Login
        self.login_button = ctk.CTkButton(
            login_frame,
            text="Entrar",
            command=self._on_login_click,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.login_button.pack(pady=(0, 20), padx=30, fill="x")
        
        # Progress bar (oculta inicialmente)
        self.progress = ctk.CTkProgressBar(login_frame)
        self.progress.pack(pady=(0, 15), padx=30, fill="x")
        self.progress.pack_forget()
        
        # Status label
        self.status_label = ctk.CTkLabel(
            login_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Separador
        separator = ctk.CTkFrame(login_frame, height=1, fg_color="gray30")
        separator.pack(pady=20, padx=30, fill="x")
        
        # Links
        links_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        links_frame.pack(pady=(0, 20))
        
        forgot_button = ctk.CTkButton(
            links_frame,
            text="Esqueci minha senha",
            fg_color="transparent",
            hover_color="gray20",
            command=self._on_forgot_password,
            width=150
        )
        forgot_button.pack(side="left", padx=5)
        
        register_button = ctk.CTkButton(
            links_frame,
            text="Criar conta",
            fg_color="transparent",
            hover_color="gray20",
            command=self._on_register,
            width=150
        )
        register_button.pack(side="left", padx=5)
        
        # Hardware ID (apenas informativo)
        hwid_frame = ctk.CTkFrame(main_frame, fg_color="gray20")
        hwid_frame.pack(pady=(20, 0), fill="x")
        
        hwid_label = ctk.CTkLabel(
            hwid_frame,
            text=f"Hardware ID: {self.hwid[:16]}...",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )
        hwid_label.pack(pady=8)
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self._on_login_click())
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
    
    def _try_auto_login(self):
        """Tenta fazer login automático com sessão salva"""
        try:
            self.status_label.configure(text="Verificando sessão...", text_color="gray")
            
            if self.auth_client.validate_session():
                self.user_data = self.auth_client.get_user_info()
                self.authenticated = True
                
                logger.info(f"✅ Login automático bem-sucedido: {self.user_data.get('email')}")
                
                self.status_label.configure(
                    text=f"✅ Bem-vindo(a), {self.user_data.get('email')}!",
                    text_color="green"
                )
                
                # Fechar janela de login após 1 segundo
                self.after(1000, self.destroy)
            else:
                self.status_label.configure(text="", text_color="gray")
                
        except Exception as e:
            logger.error(f"Erro no auto-login: {e}")
            self.status_label.configure(text="", text_color="gray")
    
    def _on_login_click(self):
        """Handler do clique no botão de login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validações
        if not email:
            messagebox.showwarning("Atenção", "Digite seu email")
            self.email_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("Atenção", "Digite sua senha")
            self.password_entry.focus()
            return
        
        # Desabilitar campos durante login
        self._set_loading(True)
        
        # Executar login em thread separada
        thread = threading.Thread(
            target=self._perform_login,
            args=(email, password),
            daemon=True
        )
        thread.start()
    
    def _perform_login(self, email: str, password: str):
        """
        Executa processo de login (em thread separada)
        
        Args:
            email: Email do usuário
            password: Senha
        """
        try:
            # Atualizar UI
            self.after(0, lambda: self.status_label.configure(
                text="Autenticando...",
                text_color="gray"
            ))
            
            # Chamar API
            result = self.auth_client.login(email, password, self.hwid)
            
            # Sucesso
            self.user_data = result.get("user")
            self.authenticated = True
            
            logger.info(f"✅ Login bem-sucedido: {email}")
            
            # Atualizar UI
            self.after(0, lambda: self._on_login_success())
            
        except AuthenticationError as e:
            # Erro de autenticação
            logger.warning(f"Falha no login: {e}")
            self.after(0, lambda: self._on_login_error(str(e)))
            
        except Exception as e:
            # Erro inesperado
            logger.exception("Erro inesperado no login")
            self.after(0, lambda: self._on_login_error(f"Erro inesperado: {str(e)}"))
    
    def _on_login_success(self):
        """Callback de sucesso no login"""
        self.status_label.configure(
            text=f"✅ Bem-vindo(a), {self.user_data.get('email')}!",
            text_color="green"
        )
        
        # Fechar janela após 1 segundo
        self.after(1000, self.destroy)
    
    def _on_login_error(self, message: str):
        """
        Callback de erro no login
        
        Args:
            message: Mensagem de erro
        """
        self._set_loading(False)
        
        self.status_label.configure(text="", text_color="gray")
        
        messagebox.showerror("Erro no Login", message)
        self.password_entry.delete(0, "end")
        self.password_entry.focus()
    
    def _set_loading(self, loading: bool):
        """
        Ativa/desativa estado de loading
        
        Args:
            loading: True para ativar, False para desativar
        """
        if loading:
            self.login_button.configure(state="disabled", text="Entrando...")
            self.email_entry.configure(state="disabled")
            self.password_entry.configure(state="disabled")
            self.progress.pack(before=self.status_label, pady=(0, 15), padx=30, fill="x")
            self.progress.start()
        else:
            self.login_button.configure(state="normal", text="Entrar")
            self.email_entry.configure(state="normal")
            self.password_entry.configure(state="normal")
            self.progress.stop()
            self.progress.pack_forget()
    
    def _on_forgot_password(self):
        """Handler para 'Esqueci minha senha'"""
        messagebox.showinfo(
            "Recuperar Senha",
            "Acesse o link abaixo para redefinir sua senha:\n\n"
            "https://kiwify.com.br/recuperar-senha"
        )
    
    def _on_register(self):
        """Handler para 'Criar conta'"""
        messagebox.showinfo(
            "Criar Conta",
            "Adquira sua licença do ClipperBot:\n\n"
            "https://kiwify.com.br/clipperbot"
        )
    
    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """
        Retorna dados do usuário autenticado
        
        Returns:
            Dicionário com dados do usuário ou None
        """
        return self.user_data
    
    def is_authenticated(self) -> bool:
        """
        Verifica se autenticação foi bem-sucedida
        
        Returns:
            True se autenticado, False caso contrário
        """
        return self.authenticated


def show_login() -> Optional[Dict[str, Any]]:
    """
    Mostra janela de login e retorna dados do usuário
    
    Returns:
        Dicionário com dados do usuário ou None se cancelado
    """
    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar e executar janela
    login_window = LoginWindow()
    login_window.mainloop()
    
    # Retornar resultado
    if login_window.is_authenticated():
        return login_window.get_user_data()
    else:
        logger.info("Login cancelado pelo usuário")
        return None


# Teste do módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🔐 Testando Tela de Login\n")
    
    user = show_login()
    
    if user:
        print(f"\n✅ Autenticado como: {user.get('email')}")
        print(f"Status: {user.get('status')}")
        print(f"Expira em: {user.get('expiration_date')}")
    else:
        print("\n❌ Login cancelado")
