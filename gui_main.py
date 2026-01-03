#!/usr/bin/env python3
"""
AutoClipper Bot - Interface Gráfica (GUI)
Branch 02: Interface moderna com CustomTkinter

Recursos:
- Download de vídeos do YouTube
- Configuração visual de palavras-chave e pesos
- Pré-visualização de parâmetros
- Execução com feedback em tempo real
- Gerenciamento de clipes gerados
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import json
from pathlib import Path
import logging

# Configuração do tema
ctk.set_appearance_mode("dark")  # "dark" ou "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

logger = logging.getLogger(__name__)


class ClipperBotGUI:
    """Interface gráfica principal do ClipperBot"""
    
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎬 ClipperBot - Cortes Inteligentes")
        self.window.geometry("1200x800")
        
        # Estado da aplicação
        self.processing = False
        self.keywords_list = []
        
        self._create_layout()
        
    def _create_layout(self):
        """Cria o layout principal da interface"""
        
        # Container principal com grid 2 colunas
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Barra lateral esquerda (configurações)
        self._create_sidebar()
        
        # Área principal direita (visualização e resultados)
        self._create_main_area()
        
    def _create_sidebar(self):
        """Cria a barra lateral com configurações"""
        
        sidebar = ctk.CTkFrame(self.window, width=350, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(8, weight=1)  # Espaço flexível
        
        # Logo/Título
        title = ctk.CTkLabel(
            sidebar, 
            text="🎬 ClipperBot", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        subtitle = ctk.CTkLabel(
            sidebar,
            text="Cortes Inteligentes com IA",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Seção 1: Entrada de Vídeo
        self._create_video_input_section(sidebar)
        
        # Seção 2: Palavras-chave
        self._create_keywords_section(sidebar)
        
        # Seção 3: Configurações Avançadas
        self._create_advanced_settings(sidebar)
        
        # Botão de Processar
        self.process_btn = ctk.CTkButton(
            sidebar,
            text="🚀 Processar Vídeo",
            command=self.start_processing,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.process_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
        
    def _create_video_input_section(self, parent):
        """Seção de entrada de vídeo"""
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        label = ctk.CTkLabel(
            input_frame,
            text="📥 Vídeo de Entrada",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # Opções de entrada
        self.input_mode = ctk.StringVar(value="url")
        
        radio_url = ctk.CTkRadioButton(
            input_frame,
            text="URL do YouTube",
            variable=self.input_mode,
            value="url",
            command=self.toggle_input_mode
        )
        radio_url.pack(padx=10, pady=5, anchor="w")
        
        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="https://youtube.com/watch?v=...",
            height=35
        )
        self.url_entry.pack(padx=10, pady=5, fill="x")
        
        radio_file = ctk.CTkRadioButton(
            input_frame,
            text="Arquivo Local",
            variable=self.input_mode,
            value="file",
            command=self.toggle_input_mode
        )
        radio_file.pack(padx=10, pady=5, anchor="w")
        
        file_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        file_frame.pack(padx=10, pady=5, fill="x")
        
        self.file_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="Caminho do arquivo...",
            height=35,
            state="disabled"
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.browse_btn = ctk.CTkButton(
            file_frame,
            text="📁",
            width=40,
            command=self.browse_file,
            state="disabled"
        )
        self.browse_btn.pack(side="right")
        
    def _create_keywords_section(self, parent):
        """Seção de palavras-chave com pesos"""
        
        keywords_frame = ctk.CTkFrame(parent)
        keywords_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        label = ctk.CTkLabel(
            keywords_frame,
            text="🔤 Palavras-Chave",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # Entry para adicionar palavras
        add_frame = ctk.CTkFrame(keywords_frame, fg_color="transparent")
        add_frame.pack(padx=10, pady=5, fill="x")
        
        self.keyword_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Digite uma palavra-chave...",
            height=35
        )
        self.keyword_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Slider de peso
        self.weight_slider = ctk.CTkSlider(
            add_frame,
            from_=1.0,
            to=3.0,
            number_of_steps=20,
            width=80
        )
        self.weight_slider.set(2.0)
        self.weight_slider.pack(side="left", padx=5)
        
        self.weight_label = ctk.CTkLabel(add_frame, text="2.0", width=35)
        self.weight_label.pack(side="left", padx=5)
        
        # Atualizar label do peso
        self.weight_slider.configure(command=self.update_weight_label)
        
        add_btn = ctk.CTkButton(
            add_frame,
            text="➕",
            width=40,
            command=self.add_keyword
        )
        add_btn.pack(side="right")
        
        # Lista de palavras adicionadas
        self.keywords_listbox = tk.Listbox(
            keywords_frame,
            height=6,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0
        )
        self.keywords_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Botões de gerenciamento
        btn_frame = ctk.CTkFrame(keywords_frame, fg_color="transparent")
        btn_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Remover",
            command=self.remove_keyword,
            width=100,
            fg_color="#dc3545",
            hover_color="#c82333"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="📋 Padrão",
            command=self.load_default_keywords,
            width=100
        ).pack(side="left", padx=2)
        
    def _create_advanced_settings(self, parent):
        """Configurações avançadas"""
        
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        label = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # Modelo Whisper
        model_label = ctk.CTkLabel(settings_frame, text="Modelo de Transcrição:")
        model_label.pack(padx=10, pady=(5, 2), anchor="w")
        
        self.model_var = ctk.StringVar(value="tiny")
        model_menu = ctk.CTkOptionMenu(
            settings_frame,
            values=["tiny", "base", "small", "medium"],
            variable=self.model_var
        )
        model_menu.pack(padx=10, pady=(0, 10), fill="x")
        
        # Número de clipes
        clips_label = ctk.CTkLabel(settings_frame, text="Número de Clipes:")
        clips_label.pack(padx=10, pady=(5, 2), anchor="w")
        
        self.clips_var = ctk.IntVar(value=5)
        clips_slider = ctk.CTkSlider(
            settings_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            variable=self.clips_var
        )
        clips_slider.pack(padx=10, pady=(0, 5), fill="x")
        
        clips_value = ctk.CTkLabel(
            settings_frame,
            textvariable=self.clips_var,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        clips_value.pack(padx=10, pady=(0, 10))
        
        # Modo rápido
        self.fast_mode = ctk.CTkSwitch(
            settings_frame,
            text="⚡ Modo Rápido",
            onvalue=True,
            offvalue=False
        )
        self.fast_mode.select()  # Ativado por padrão
        self.fast_mode.pack(padx=10, pady=5, anchor="w")
        
        # Margem de segurança
        margin_label = ctk.CTkLabel(settings_frame, text="Margem de Segurança (s):")
        margin_label.pack(padx=10, pady=(10, 2), anchor="w")
        
        self.margin_var = ctk.IntVar(value=8)
        margin_slider = ctk.CTkSlider(
            settings_frame,
            from_=5,
            to=15,
            number_of_steps=10,
            variable=self.margin_var
        )
        margin_slider.pack(padx=10, pady=(0, 5), fill="x")
        
        margin_value = ctk.CTkLabel(
            settings_frame,
            textvariable=self.margin_var,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        margin_value.pack(padx=10, pady=(0, 10))
        
    def _create_main_area(self):
        """Cria a área principal com tabs"""
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Tabs
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        
        # Tab 1: Preview/Status
        self.tab_preview = self.tabview.add("📊 Status")
        self._create_preview_tab()
        
        # Tab 2: Resultados
        self.tab_results = self.tabview.add("🎬 Resultados")
        self._create_results_tab()
        
        # Tab 3: Logs
        self.tab_logs = self.tabview.add("📝 Logs")
        self._create_logs_tab()
        
    def _create_preview_tab(self):
        """Tab de preview e status"""
        
        # Frame de status
        status_frame = ctk.CTkFrame(self.tab_preview)
        status_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Aguardando configuração...",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=20)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(padx=40, pady=10, fill="x")
        self.progress_bar.set(0)
        
        # Área de informações
        self.info_text = ctk.CTkTextbox(
            status_frame,
            height=400,
            font=ctk.CTkFont(size=12)
        )
        self.info_text.pack(padx=20, pady=20, fill="both", expand=True)
        self.info_text.insert("1.0", "🎬 Bem-vindo ao ClipperBot!\n\n")
        self.info_text.insert("end", "Configure as opções na barra lateral e clique em 'Processar Vídeo'.\n\n")
        self.info_text.insert("end", "Recursos:\n")
        self.info_text.insert("end", "✓ Sistema de pesos para palavras-chave\n")
        self.info_text.insert("end", "✓ Detecção de frases completas\n")
        self.info_text.insert("end", "✓ Margem de segurança configurável\n")
        self.info_text.insert("end", "✓ Processamento rápido e eficiente\n")
        self.info_text.configure(state="disabled")
        
    def _create_results_tab(self):
        """Tab de resultados"""
        
        results_frame = ctk.CTkFrame(self.tab_results)
        results_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        label = ctk.CTkLabel(
            results_frame,
            text="Clipes gerados aparecerão aqui",
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=20)
        
        # Lista de clipes
        self.results_listbox = tk.Listbox(
            results_frame,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            font=("Segoe UI", 11),
            relief="flat",
            borderwidth=0
        )
        self.results_listbox.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        btn_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="📂 Abrir Pasta",
            command=self.open_output_folder
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="▶️ Reproduzir",
            command=self.play_selected_clip
        ).pack(side="left", padx=5)
        
    def _create_logs_tab(self):
        """Tab de logs"""
        
        logs_frame = ctk.CTkFrame(self.tab_logs)
        logs_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.logs_text = ctk.CTkTextbox(
            logs_frame,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.logs_text.pack(padx=10, pady=10, fill="both", expand=True)
        
    # Event Handlers
    
    def toggle_input_mode(self):
        """Alterna entre URL e arquivo local"""
        mode = self.input_mode.get()
        if mode == "url":
            self.url_entry.configure(state="normal")
            self.file_entry.configure(state="disabled")
            self.browse_btn.configure(state="disabled")
        else:
            self.url_entry.configure(state="disabled")
            self.file_entry.configure(state="normal")
            self.browse_btn.configure(state="normal")
    
    def browse_file(self):
        """Abre diálogo para selecionar arquivo"""
        filename = filedialog.askopenfilename(
            title="Selecionar Vídeo",
            filetypes=[
                ("Vídeos", "*.mp4 *.avi *.mkv *.mov"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
    
    def update_weight_label(self, value):
        """Atualiza o label do peso"""
        self.weight_label.configure(text=f"{value:.1f}")
    
    def add_keyword(self):
        """Adiciona palavra-chave à lista"""
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            return
        
        weight = self.weight_slider.get()
        self.keywords_list.append({"keyword": keyword, "weight": weight})
        
        # Adicionar à listbox
        self.keywords_listbox.insert(tk.END, f"{keyword} (peso: {weight:.1f})")
        
        # Limpar entry
        self.keyword_entry.delete(0, tk.END)
        self.weight_slider.set(2.0)
        self.update_weight_label(2.0)
    
    def remove_keyword(self):
        """Remove palavra-chave selecionada"""
        selection = self.keywords_listbox.curselection()
        if selection:
            index = selection[0]
            self.keywords_listbox.delete(index)
            del self.keywords_list[index]
    
    def load_default_keywords(self):
        """Carrega palavras-chave padrão"""
        defaults = [
            {"keyword": "milhão", "weight": 2.5},
            {"keyword": "segredo", "weight": 3.0},
            {"keyword": "importante", "weight": 2.5},
            {"keyword": "incrível", "weight": 2.0},
            {"keyword": "atenção", "weight": 1.0}
        ]
        
        self.keywords_listbox.delete(0, tk.END)
        self.keywords_list.clear()
        
        for item in defaults:
            self.keywords_list.append(item)
            self.keywords_listbox.insert(
                tk.END,
                f"{item['keyword']} (peso: {item['weight']:.1f})"
            )
    
    def start_processing(self):
        """Inicia o processamento do vídeo"""
        # Validações
        if not self.keywords_list:
            messagebox.showwarning(
                "Atenção",
                "Adicione pelo menos uma palavra-chave!"
            )
            return
        
        mode = self.input_mode.get()
        if mode == "url":
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning(
                    "Atenção",
                    "Insira uma URL do YouTube!"
                )
                return
        else:
            filepath = self.file_entry.get().strip()
            if not filepath or not Path(filepath).exists():
                messagebox.showwarning(
                    "Atenção",
                    "Selecione um arquivo válido!"
                )
                return
        
        # Iniciar processamento em thread separada
        self.processing = True
        self.process_btn.configure(state="disabled", text="⏳ Processando...")
        
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def process_video(self):
        """Processa o vídeo (thread separada)"""
        # TODO: Implementar integração com o backend
        self.log("Iniciando processamento...")
        self.update_status("Preparando ambiente...")
        
        # Placeholder - será implementado na próxima etapa
        import time
        for i in range(100):
            time.sleep(0.05)
            self.progress_bar.set(i / 100)
            if i % 20 == 0:
                self.log(f"Progresso: {i}%")
        
        self.log("Processamento concluído!")
        self.update_status("✅ Processamento concluído!")
        self.process_btn.configure(state="normal", text="🚀 Processar Vídeo")
        self.processing = False
    
    def update_status(self, text):
        """Atualiza o status"""
        self.status_label.configure(text=text)
    
    def log(self, message):
        """Adiciona mensagem ao log"""
        self.logs_text.insert("end", f"{message}\n")
        self.logs_text.see("end")
    
    def open_output_folder(self):
        """Abre a pasta de saída"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def play_selected_clip(self):
        """Reproduz o clipe selecionado"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def run(self):
        """Inicia a aplicação"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ClipperBotGUI()
    app.run()
