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
import os
import sys
from datetime import datetime

# Importar módulos do backend
from src.downloader import VideoDownloader
from src.transcriber import AudioTranscriber
from src.analyzer import ClimaxAnalyzer
from src.video_cutter import VideoCutter

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
        self.output_folder = None
        
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
        try:
            self.log("🎬 Iniciando processamento...")
            self.update_status("Preparando ambiente...")
            self.progress_bar.set(0.05)
            
            # Obter configurações
            mode = self.input_mode.get()
            video_url = self.url_entry.get().strip() if mode == "url" else None
            video_file = self.file_entry.get().strip() if mode == "file" else None
            
            # Preparar palavras-chave e pesos
            keywords = [item["keyword"] for item in self.keywords_list]
            keyword_weights = {item["keyword"]: item["weight"] for item in self.keywords_list}
            
            model_size = self.model_var.get()
            max_clips = self.clips_var.get()
            fast_mode = self.fast_mode.get()
            safety_margin = self.margin_var.get()
            
            self.log(f"📋 Configurações:")
            self.log(f"   - Palavras-chave: {', '.join(keywords)}")
            self.log(f"   - Modelo: {model_size}")
            self.log(f"   - Clipes: {max_clips}")
            self.log(f"   - Modo rápido: {'Sim' if fast_mode else 'Não'}")
            self.log(f"   - Margem de segurança: {safety_margin}s")
            self.log("")
            
            # ETAPA 1: Download
            self.log("📥 ETAPA 1: Download")
            self.update_status("📥 Baixando vídeo...")
            self.progress_bar.set(0.1)
            
            downloader = VideoDownloader(output_dir="downloads")
            
            if video_url:
                self.log(f"   URL: {video_url}")
                info = downloader.get_video_info(video_url)
                if info:
                    self.log(f"   📹 Título: {info['title']}")
                    self.log(f"   ⏱️ Duração: {info['duration']}s ({info['duration']/60:.1f} min)")
                
                video_path = downloader.download_video(video_url)
                audio_path = downloader.download_audio(video_url, format='wav')
            else:
                self.log(f"   Arquivo: {video_file}")
                video_path = video_file
                # Extrair áudio do arquivo local
                audio_path = downloader.extract_audio(video_file)
            
            if not video_path or not audio_path:
                raise Exception("Falha no download/extração de áudio")
            
            self.log(f"   ✅ Vídeo: {Path(video_path).name}")
            self.log(f"   ✅ Áudio: {Path(audio_path).name}")
            self.log("")
            self.progress_bar.set(0.25)
            
            # ETAPA 2: Transcrição
            self.log("🎤 ETAPA 2: Transcrição")
            self.update_status("🎤 Transcrevendo áudio...")
            
            transcriber = AudioTranscriber(
                model_size=model_size,
                use_cache=fast_mode
            )
            
            self.log(f"   Usando modelo: {model_size}")
            if fast_mode:
                self.log("   ⚡ Cache ativado")
            
            transcription = transcriber.transcribe(
                audio_path,
                language='pt',
                word_timestamps=True
            )
            
            if not transcription:
                raise Exception("Falha na transcrição")
            
            self.log(f"   ✅ {len(transcription)} segmentos transcritos")
            full_text = transcriber.get_full_text(transcription)
            self.log(f"   ✅ {len(full_text)} caracteres de texto")
            self.log("")
            self.progress_bar.set(0.5)
            
            # ETAPA 3: Análise de Clímax
            self.log("🔍 ETAPA 3: Análise de Clímax")
            self.update_status("🔍 Analisando momentos...")
            
            analyzer = ClimaxAnalyzer(
                keywords_climax=keywords,
                keyword_weights=keyword_weights,
                keywords_ignore=['patrocinador', 'inscreva-se', 'anúncio'],
                min_volume_db=-10.0,
                cut_duration_min=30,
                cut_duration_max=90,
                safety_margin=safety_margin
            )
            
            # Análise semântica
            self.log(f"   🔤 Buscando palavras-chave...")
            semantic_moments = analyzer.analyze_semantic(transcription)
            self.log(f"   ✅ {len(semantic_moments)} momentos semânticos encontrados")
            
            # Análise acústica
            self.log(f"   🔊 Analisando picos de volume...")
            acoustic_moments = analyzer.analyze_acoustic(audio_path, fast_mode=fast_mode)
            self.log(f"   ✅ {len(acoustic_moments)} picos acústicos encontrados")
            
            # Combinar análises
            all_moments = analyzer.combine_analyses(semantic_moments, acoustic_moments)
            self.log(f"   ✅ {len(all_moments)} momentos totais identificados")
            
            # Criar pontos de corte
            cut_points = analyzer.create_cut_points(all_moments)
            
            # Limitar número de clipes
            if len(cut_points) > max_clips:
                self.log(f"   ⚠️ Limitando para os {max_clips} melhores momentos")
                cut_points = cut_points[:max_clips]
            
            self.log("")
            self.log("   📋 Pontos de Corte:")
            for i, cut in enumerate(cut_points, 1):
                self.log(f"      {i}. [{cut['start']:.1f}s - {cut['end']:.1f}s] ({cut['duration']:.1f}s) - {cut['reason']}")
            self.log("")
            self.progress_bar.set(0.7)
            
            # ETAPA 4: Corte de Vídeo
            self.log("✂️ ETAPA 4: Corte de Vídeo")
            self.update_status("✂️ Gerando clipes...")
            
            # Criar pasta de saída com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"output_clips_{timestamp}"
            
            cutter = VideoCutter(output_dir=output_dir)
            
            self.log(f"   📁 Pasta de saída: {output_dir}")
            self.log(f"   🎬 Processando {len(cut_points)} clipes...")
            
            output_files = cutter.cut_multiple_segments(
                input_video=video_path,
                cut_points=cut_points,
                prefix="clip",
                parallel=fast_mode,
                max_workers=3
            )
            
            self.log(f"   ✅ {len(output_files)} clipes gerados!")
            self.log("")
            self.progress_bar.set(1.0)
            
            # Exibir resultados
            self.log("" + "="*50)
            self.log("📊 RESUMO FINAL")
            self.log("="*50)
            self.log(f"Clipes gerados: {len(output_files)}")
            self.log(f"Pasta de saída: {output_dir}")
            self.log("")
            self.log("Arquivos:")
            
            # Adicionar à lista de resultados
            self.output_folder = output_dir
            self.results_listbox.delete(0, tk.END)
            
            for i, file_path in enumerate(output_files, 1):
                file_name = Path(file_path).name
                size_mb = Path(file_path).stat().st_size / (1024 * 1024)
                self.log(f"  {i}. {file_name} ({size_mb:.1f} MB)")
                self.results_listbox.insert(tk.END, f"{i}. {file_name} ({size_mb:.1f} MB)")
            
            self.log("")
            self.log("🎉 Processamento concluído com sucesso!")
            self.log("" + "="*50)
            
            self.update_status(f"✅ {len(output_files)} clipes gerados!")
            
            # Mostrar mensagem de sucesso
            self.window.after(0, lambda: messagebox.showinfo(
                "Sucesso!",
                f"{len(output_files)} clipes foram gerados com sucesso!\n\nPasta: {output_dir}"
            ))
            
            # Mudar para aba de resultados
            self.window.after(0, lambda: self.tabview.set("🎬 Resultados"))
            
        except Exception as e:
            self.log(f"")
            self.log(f"❌ ERRO: {str(e)}")
            self.log(f"")
            self.update_status("❌ Erro no processamento")
            self.window.after(0, lambda: messagebox.showerror(
                "Erro",
                f"Ocorreu um erro durante o processamento:\n\n{str(e)}"
            ))
        
        finally:
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
        if hasattr(self, 'output_folder') and Path(self.output_folder).exists():
            if sys.platform == 'win32':
                os.startfile(self.output_folder)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{self.output_folder}"')
            else:  # linux
                os.system(f'xdg-open "{self.output_folder}"')
        else:
            messagebox.showwarning(
                "Atenção",
                "Nenhuma pasta de saída encontrada.\nProcesse um vídeo primeiro!"
            )
    
    def play_selected_clip(self):
        """Reproduz o clipe selecionado"""
        selection = self.results_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Atenção",
                "Selecione um clipe para reproduzir!"
            )
            return
        
        if not hasattr(self, 'output_folder'):
            messagebox.showwarning(
                "Atenção",
                "Nenhuma pasta de saída encontrada!"
            )
            return
        
        # Obter o nome do arquivo da listbox
        item_text = self.results_listbox.get(selection[0])
        # Extrair nome do arquivo (formato: "1. clip_001.mp4 (5.2 MB)")
        filename = item_text.split('. ', 1)[1].rsplit(' (', 1)[0]
        
        file_path = Path(self.output_folder) / filename
        
        if file_path.exists():
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{file_path}"')
            else:  # linux
                os.system(f'xdg-open "{file_path}"')
        else:
            messagebox.showerror(
                "Erro",
                f"Arquivo não encontrado:\n{file_path}"
            )
    
    def run(self):
        """Inicia a aplicação"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ClipperBotGUI()
    app.run()
