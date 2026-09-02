#!/usr/bin/env python3
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
import re
from datetime import datetime
from PIL import Image, ImageTk
import subprocess

class JSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("BLANCH.CC JSON EDITOR [TERMINAL MODE]")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Configurar estilo terminal Linux
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Paleta de colores terminal
        self.colors = {
            'bg': '#000000',
            'bg_card': '#1a1a1a',
            'bg_hover': '#2d2d2d',
            'accent': '#00ff00',
            'accent_secondary': '#008000',
            'text_primary': '#00ff00',
            'text_secondary': '#00b300',
            'border': '#00ff00',
            'success': '#00ff00',
            'warning': '#ffff00',
            'error': '#ff0000',
            'info': '#00ffff'
        }
        
        # Fuente monoespaciada estilo terminal
        self.terminal_font = ('Courier New', 10)
        self.terminal_font_bold = ('Courier New', 10, 'bold')
        self.terminal_font_small = ('Courier New', 9)
        
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text_primary'], font=self.terminal_font)
        self.style.configure('TButton', background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=self.terminal_font_bold, borderwidth=1)
        self.style.map('TButton', background=[('active', self.colors['bg_hover']), ('pressed', self.colors['accent'])], foreground=[('pressed', '#000000')])
        self.style.configure('TNotebook', background=self.colors['bg'])
        self.style.configure('TNotebook.Tab', background=self.colors['bg_card'], foreground=self.colors['text_secondary'], padding=[8, 4], font=self.terminal_font_bold, borderwidth=1)
        self.style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])], foreground=[('selected', '#000000')])
        
        self.root.configure(bg=self.colors['bg'])
        
        # Ruta base del proyecto
        self.base_path = Path(__file__).parent / 'src' / 'data'
        self.public_path = Path(__file__).parent / 'public'
        self.project_root = Path(__file__).parent
        self.cert_images = {}
        
        # Archivos JSON disponibles
        self.json_files = {
            'CERT': 'certifications.json',
            'POSTS': 'posts.json',
            'PROJ': 'projects.json',
            'SEC': 'secondary-projects.json',
            'SRV': 'services.json',
            'IDEAS': 'ideas.json'
        }
        
        self.current_data = None
        self.current_file = None
        self.unsaved_changes = False
        self.showing_dashboard = True
        
        # Archivo de ideas
        self.ideas_file = self.base_path / 'ideas.json'
        self.ideas_data = []
        self.current_idea_id = None
        
        # Campos específicos para ideas
        self.idea_post_data = {}
        self.idea_project_data = {}
        self.idea_certification_data = {}
        self.idea_secondary_project_data = {}
        
        # Sistema de notificaciones no intrusivas
        self.notification_timer = None
        self.notification_queue = []
        self.showing_notification = False
        
        self.create_ui()
        self.show_dashboard()
    
    def create_ui(self):
        # Frame principal - más compacto
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header estilo terminal - muy compacto
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 2))
        
        # Línea estilo terminal
        tk.Frame(header_frame, bg=self.colors['border'], height=1).pack(fill=tk.X)
        
        self.title_label = tk.Label(header_frame, text="[BLANCH.CC] JSON EDITOR >", 
                              font=self.terminal_font_bold, bg=self.colors['bg'], fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT, padx=2)
        
        # Botón de cierre estilo terminal
        close_btn = tk.Button(header_frame, text="[X]", 
                            command=self.root.destroy,
                            font=self.terminal_font_bold, 
                            bg=self.colors['bg'], fg=self.colors['error'], 
                            activebackground=self.colors['error'], activeforeground='#000000',
                            relief=tk.FLAT, cursor='hand2', bd=1, padx=5, pady=2)
        close_btn.pack(side=tk.RIGHT)
        
        # Selector de archivo estilo terminal - muy compacto
        selector_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        selector_frame.pack(fill=tk.X, pady=(0, 2))
        
        # Grid de botones estilo terminal
        self.file_buttons = {}
        button_grid = tk.Frame(selector_frame, bg=self.colors['bg'])
        button_grid.pack(fill=tk.X)
        
        btn_style_terminal = {'font': self.terminal_font_bold, 'bg': self.colors['bg'], 'fg': self.colors['text_secondary'], 
                          'activebackground': self.colors['accent'], 'activeforeground': '#000000',
                          'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 4, 'pady': 2,
                          'highlightbackground': self.colors['border'], 'highlightthickness': 1}
        
        for idx, (name, file) in enumerate(self.json_files.items()):
            btn = tk.Button(button_grid, text=f"[{name}]", 
                          command=lambda f=file: self.load_specific_file(f),
                          **btn_style_terminal)
            btn.grid(row=0, column=idx, padx=1, pady=0, sticky='ew')
            button_grid.grid_columnconfigure(idx, weight=1)
            self.file_buttons[file] = btn
        
        # Botones de acción estilo terminal - muy compactos
        action_btn_frame = tk.Frame(selector_frame, bg=self.colors['bg'])
        action_btn_frame.pack(fill=tk.X, pady=(2, 0))
        
        btn_style_action = {'font': self.terminal_font_bold, 'bg': self.colors['success'], 'fg': '#000000', 
                           'activebackground': '#00cc00', 'activeforeground': '#000000',
                           'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 8, 'pady': 2}
        
        btn_style_secondary = {'font': self.terminal_font_bold, 'bg': self.colors['bg_card'], 'fg': self.colors['text_primary'], 
                           'activebackground': self.colors['bg_hover'], 'activeforeground': self.colors['text_primary'],
                           'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 8, 'pady': 2}
        
        btn_style_primary = {'font': self.terminal_font_bold, 'bg': self.colors['accent'], 'fg': '#000000', 
                           'activebackground': '#00cc00', 'activeforeground': '#000000',
                           'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 8, 'pady': 2}
        
        btn_style_danger = {'font': self.terminal_font_bold, 'bg': self.colors['error'], 'fg': '#000000', 
                           'activebackground': '#cc0000', 'activeforeground': '#000000',
                           'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 8, 'pady': 2}
        
        tk.Button(action_btn_frame, text="[+]ADD", command=self.add_element, **btn_style_primary).pack(side=tk.LEFT, padx=1)
        tk.Button(action_btn_frame, text="[S]SAVE", command=self.save_file, **btn_style_action).pack(side=tk.LEFT, padx=1)
        tk.Button(action_btn_frame, text="[R]REFRESH", command=self.refresh_file, **btn_style_secondary).pack(side=tk.LEFT, padx=1)
        tk.Button(action_btn_frame, text="[E]EDIT", command=self.edit_element, **btn_style_primary).pack(side=tk.LEFT, padx=1)
        tk.Button(action_btn_frame, text="[D]DELETE", command=self.delete_element, **btn_style_danger).pack(side=tk.LEFT, padx=1)
        
        # Notebook para diferentes vistas - estilo terminal compacto
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Vista dashboard
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text='[DASH]')
        
        # Vista visual por tipo de JSON
        self.visual_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visual_frame, text='[VIEW]')
        
        # Editor de texto para JSON raw
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='[RAW]')
        
        # Editor de elementos
        self.editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text='[EDIT]')
        
        self.create_visual_view()
        self.create_text_editor()
        self.create_dashboard()
        self.create_element_editor()
        
        # Configurar atajos de teclado mejorados
        self.setup_keyboard_shortcuts()
        
        # Línea decorativa terminal
        tk.Frame(main_frame, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=(2, 1))
        
        # Status bar estilo terminal
        self.status_var = tk.StringVar()
        self.status_var.set("READY > Select file to begin")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                            font=self.terminal_font_small, bg=self.colors['bg'], fg=self.colors['text_secondary'], 
                            relief=tk.FLAT, pady=1, anchor='w')
        status_bar.pack(fill=tk.X)
        
        # Indicador de cambios sin guardar
        self.unsaved_label = tk.Label(main_frame, text="", 
                                     font=self.terminal_font_small, 
                                     bg=self.colors['bg'], fg=self.colors['warning'], anchor='w')
        self.unsaved_label.pack(fill=tk.X, pady=(0, 1))
        
    
    def create_visual_canvas(self):
        """Recrear el canvas visual después de destruirlo"""
        # Limpiar visual_frame primero
        for widget in self.visual_frame.winfo_children():
            widget.destroy()
        self.create_visual_view()
    
    def create_visual_view(self):
        # Scrollbars estilo terminal
        visual_scroll_y = ttk.Scrollbar(self.visual_frame)
        visual_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        visual_scroll_x = ttk.Scrollbar(self.visual_frame, orient=tk.HORIZONTAL)
        visual_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas para vista visual
        self.visual_canvas = tk.Canvas(self.visual_frame, bg=self.colors['bg'], yscrollcommand=visual_scroll_y.set, xscrollcommand=visual_scroll_x.set, highlightthickness=1, highlightbackground=self.colors['border'])
        self.visual_canvas.pack(fill=tk.BOTH, expand=True)
        
        visual_scroll_y.config(command=self.visual_canvas.yview)
        visual_scroll_x.config(command=self.visual_canvas.xview)
        
        self.visual_elements = []
        self.selected_element = None
        self.hovered_element = None
        
        # Bind events para selección y edición
        self.visual_canvas.bind('<Button-1>', self.on_canvas_click)
        self.visual_canvas.bind('<Double-Button-1>', self.on_canvas_double_click)
        self.visual_canvas.bind('<Motion>', self.on_canvas_hover)
        
        # Bind events para scroll del ratón
        try:
            self.visual_canvas.bind('<MouseWheel>', lambda e: self.visual_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        except:
            pass
        self.visual_canvas.bind('<Button-4>', lambda e: self.visual_canvas.yview_scroll(-1, "units"))
        self.visual_canvas.bind('<Button-5>', lambda e: self.visual_canvas.yview_scroll(1, "units"))
    
    def create_text_editor(self):
        # Scrollbar
        text_scroll = ttk.Scrollbar(self.text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget estilo terminal
        self.text_editor = tk.Text(self.text_frame, yscrollcommand=text_scroll.set, bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=self.terminal_font, insertbackground=self.colors['accent'], relief=tk.FLAT, bd=1)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Detectar cambios en el editor de texto
        self.text_editor.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        
        text_scroll.config(command=self.text_editor.yview)
    
    def create_ideas_interface(self):
        """Crear interfaz específica para ideas - estilo terminal puro"""
        ideas_frame = tk.Frame(self.visual_frame, bg=self.colors['bg'])
        ideas_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Header simple
        header_frame = tk.Frame(ideas_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 2))
        
        tk.Label(header_frame, text="ideas.txt", font=self.terminal_font_bold,
                bg=self.colors['bg'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Botones básicos
        btn_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        btn_frame.pack(side=tk.RIGHT)
        
        btn_style = {'font': self.terminal_font_bold, 'bg': self.colors['bg_card'], 'fg': self.colors['text_primary'],
                     'activebackground': self.colors['bg_hover'], 'activeforeground': self.colors['text_primary'],
                     'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 4, 'pady': 1}
        
        tk.Button(btn_frame, text="[N]ew", command=self.new_idea, **btn_style).pack(side=tk.LEFT, padx=1)
        tk.Button(btn_frame, text="[S]ave", command=self.save_idea, **btn_style).pack(side=tk.LEFT, padx=1)
        tk.Button(btn_frame, text="[D]el", command=self.delete_idea, **btn_style).pack(side=tk.LEFT, padx=1)
        
        # Split: lista izquierda, editor derecha
        split_frame = tk.Frame(ideas_frame, bg=self.colors['bg'])
        split_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de ideas (checklist estilo terminal)
        list_frame = tk.Frame(split_frame, bg=self.colors['bg'], width=300)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 2))
        
        self.ideas_listbox = tk.Listbox(list_frame, bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                                        font=self.terminal_font, relief=tk.FLAT, bd=1,
                                        selectbackground=self.colors['accent'], selectforeground='#000000')
        self.ideas_listbox.pack(fill=tk.BOTH, expand=True)
        self.ideas_listbox.bind('<<ListboxSelect>>', self.on_idea_selected)
        
        # Editor de texto plano
        editor_frame = tk.Frame(split_frame, bg=self.colors['bg'])
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.idea_content_text = tk.Text(editor_frame, bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                                        insertbackground=self.colors['accent'], font=self.terminal_font, 
                                        relief=tk.FLAT, bd=1, wrap=tk.WORD)
        self.idea_content_text.pack(fill=tk.BOTH, expand=True)
        
        # Auto-save al escribir
        self.idea_content_text.bind('<KeyRelease>', self.on_idea_key_release)
        self.idea_autosave_timer = None
        
        # Campo para prompt (oculto, solo para compatibilidad)
        self.prompt_text = tk.Text(editor_frame, height=0, width=0, bg=self.colors['bg'], fg=self.colors['bg'])
        
        # Cargar ideas
        self.load_ideas()
    
    def show_notification(self, message, message_type='info'):
        """Mostrar notificación no intrusiva en la status bar"""
        # Cancelar timer anterior si existe
        if self.notification_timer:
            self.root.after_cancel(self.notification_timer)
            self.notification_timer = None
        
        # Determinar color según tipo
        color = self.colors['info']
        if message_type == 'success':
            color = self.colors['success']
        elif message_type == 'warning':
            color = self.colors['warning']
        elif message_type == 'error':
            color = self.colors['error']
        
        # Mostrar mensaje
        self.status_var.set(f"[{message_type.upper()}] {message}")
        self.status_bar = self.root.winfo_children()[0].winfo_children()[-2]  # Status bar
        self.status_bar.config(fg=color)
        
        # Auto-cerrar después de 3 segundos
        self.notification_timer = self.root.after(3000, self.clear_notification)
    
    def clear_notification(self):
        """Limpiar notificación y restaurar estado normal"""
        self.status_var.set("READY >")
        self.status_bar.config(fg=self.colors['text_secondary'])
        self.notification_timer = None
    
    def create_element_editor(self):
        # Scrollable frame para el editor
        self.editor_scroll_y = ttk.Scrollbar(self.editor_frame)
        self.editor_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.editor_canvas = tk.Canvas(self.editor_frame, bg=self.colors['bg'], yscrollcommand=self.editor_scroll_y.set, highlightthickness=1, highlightbackground=self.colors['border'])
        self.editor_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.editor_scroll_y.config(command=self.editor_canvas.yview)
        
        # Bind para scroll con ratón
        try:
            self.editor_canvas.bind('<MouseWheel>', lambda e: self.editor_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        except:
            pass
        self.editor_canvas.bind('<Button-4>', lambda e: self.editor_canvas.yview_scroll(-1, "units"))
        self.editor_canvas.bind('<Button-5>', lambda e: self.editor_canvas.yview_scroll(1, "units"))
        
        self.editor_scrollable_frame = tk.Frame(self.editor_canvas, bg=self.colors['bg'])
        self.editor_canvas.create_window((0, 0), window=self.editor_scrollable_frame, anchor="nw")
        
        self.editor_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))
        )
        
        self.editor_entries = {}
        self.editor_mode = None  # 'add' or 'edit'
        self.editor_element = None
        
        # Botones de acción del editor estilo terminal
        self.editor_button_frame = tk.Frame(self.editor_scrollable_frame, bg=self.colors['bg'])
        self.editor_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_style_save = {'font': self.terminal_font_bold, 'bg': self.colors['success'], 'fg': '#000000', 
                     'activebackground': '#00cc00', 'activeforeground': '#000000',
                     'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 12, 'pady': 4}
        
        btn_style_cancel = {'font': self.terminal_font_bold, 'bg': self.colors['bg_card'], 'fg': self.colors['text_primary'], 
                     'activebackground': self.colors['bg_hover'], 'activeforeground': self.colors['text_primary'],
                     'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 12, 'pady': 4}
        
        tk.Button(self.editor_button_frame, text="[S]SAVE", command=self.save_editor, **btn_style_save).pack(side=tk.LEFT, padx=1)
        tk.Button(self.editor_button_frame, text="[ESC]CANCEL", command=self.cancel_editor, **btn_style_cancel).pack(side=tk.LEFT, padx=1)
    
    def create_dashboard(self):
        # Frame principal del dashboard - compacto
        dash_main = tk.Frame(self.dashboard_frame, bg=self.colors['bg'])
        dash_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Título del dashboard estilo terminal
        title_frame = tk.Frame(dash_main, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(title_frame, text="[DASHBOARD] >", 
                font=self.terminal_font_bold, bg=self.colors['bg'], fg=self.colors['text_primary']).pack(anchor=tk.W)
        tk.Label(title_frame, text="Statistics & Quick Actions", 
                font=self.terminal_font_small, bg=self.colors['bg'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(2, 0))
        
        # Frame para estadísticas - compacto
        stats_frame = tk.Frame(dash_main, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Cargar estadísticas
        self.dashboard_stats = {}
        for name, file in self.json_files.items():
            try:
                file_path = self.base_path / file
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.dashboard_stats[name] = len(data)
                    elif isinstance(data, dict):
                        if file == 'secondary-projects.json':
                            total = sum(len(v) if isinstance(v, list) else 1 for v in data.values())
                            self.dashboard_stats[name] = total
                        else:
                            self.dashboard_stats[name] = len(data)
            except:
                self.dashboard_stats[name] = 0
        
        # Crear tarjetas de estadísticas estilo terminal
        stats_grid = tk.Frame(stats_frame, bg=self.colors['bg'])
        stats_grid.pack(fill=tk.X)
        
        for idx, (name, count) in enumerate(self.dashboard_stats.items()):
            card = tk.Frame(stats_grid, bg=self.colors['bg_card'], bd=1, relief=tk.FLAT, highlightbackground=self.colors['border'], highlightthickness=1)
            card.grid(row=0, column=idx, padx=2, pady=2, sticky='nsew')
            stats_grid.grid_columnconfigure(idx, weight=1)
            
            tk.Label(card, text=name, font=self.terminal_font_bold, 
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=(5, 2))
            tk.Label(card, text=str(count), font=self.terminal_font_bold, 
                    bg=self.colors['bg_card'], fg=self.colors['accent']).pack(pady=(0, 5))
            
            # Hacer la tarjeta clickeable
            card.bind('<Button-1>', lambda e, f=self.json_files[name]: self.load_specific_file(f))
        
        # Frame para acciones rápidas - compacto
        actions_frame = tk.Frame(dash_main, bg=self.colors['bg'])
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(actions_frame, text="[QUICK ACTIONS] >", 
                font=self.terminal_font_bold, bg=self.colors['bg'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0, 5))
        
        # Botones compactos para cargar archivos
        btn_grid = tk.Frame(actions_frame, bg=self.colors['bg'])
        btn_grid.pack(fill=tk.BOTH, expand=True)
        
        btn_style_large = {'font': self.terminal_font_bold, 'bg': self.colors['bg_card'], 'fg': self.colors['text_primary'], 
                          'activebackground': self.colors['accent'], 'activeforeground': '#000000',
                          'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 1, 'padx': 8, 'pady': 6,
                          'highlightbackground': self.colors['border'], 'highlightthickness': 1}
        
        for idx, (name, file) in enumerate(self.json_files.items()):
            btn = tk.Button(btn_grid, text=f"[{name}]", 
                          command=lambda f=file: self.load_specific_file(f),
                          **btn_style_large)
            btn.grid(row=idx // 3, column=idx % 3, padx=2, pady=2, sticky='nsew')
        
        for i in range(3):
            btn_grid.grid_columnconfigure(i, weight=1)
        for i in range(2):
            btn_grid.grid_rowconfigure(i, weight=1)
    
    def show_dashboard(self):
        self.notebook.select(0)
    
    def load_specific_file(self, json_file):
        # Verificar si hay cambios sin guardar
        if self.unsaved_changes:
            # Usar notificación en lugar de messagebox
            self.show_notification("Unsaved changes - auto-saving...", "warning")
            self.save_file()
        
        file_path = self.base_path / json_file
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.current_file = json_file
            self.current_data = data
            
            # Si es ideas.json, usar interfaz especial
            if json_file == 'ideas.json':
                # Limpiar visual frame y crear interfaz de ideas
                for widget in self.visual_frame.winfo_children():
                    widget.destroy()
                self.create_ideas_interface()
                # No actualizar text editor para ideas.json
                self.show_notification(f"Loaded: {json_file}", "success")
                self.unsaved_changes = False
                self.unsaved_label.config(text="")
            else:
                # Si venimos de ideas.json, recrear el canvas visual
                if not hasattr(self, 'visual_canvas') or not self.visual_canvas.winfo_exists():
                    self.create_visual_canvas()
                self.update_visual_view()
                self.update_text_editor()
                self.show_notification(f"Loaded: {json_file}", "success")
                self.unsaved_changes = False
                self.unsaved_label.config(text="")
            
            # Actualizar botones para mostrar el archivo activo
            for file, btn in self.file_buttons.items():
                if file == json_file:
                    btn.config(bg=self.colors['accent'], fg='#ffffff', activebackground='#1f6feb')
                else:
                    btn.config(bg=self.colors['bg_card'], fg=self.colors['text_secondary'], activebackground=self.colors['bg_hover'])
            
            # Cambiar automáticamente a la vista visual al cargar un archivo
            self.notebook.select(1)
            
        except FileNotFoundError:
            # Para ideas.json, crear el archivo si no existe
            if json_file == 'ideas.json':
                self.current_data = []
                self.current_file = json_file
                # Limpiar visual frame y crear interfaz de ideas
                for widget in self.visual_frame.winfo_children():
                    widget.destroy()
                self.create_ideas_interface()
                self.update_text_editor()
                self.show_notification(f"Created: {json_file}", "success")
                self.unsaved_changes = False
                self.unsaved_label.config(text="")
                
                # Actualizar botones para mostrar el archivo activo
                for file, btn in self.file_buttons.items():
                    if file == json_file:
                        btn.config(bg=self.colors['accent'], fg='#ffffff', activebackground='#1f6feb')
                    else:
                        btn.config(bg=self.colors['bg_card'], fg=self.colors['text_secondary'], activebackground=self.colors['bg_hover'])
                
                self.notebook.select(1)
            else:
                self.show_notification(f"File not found: {file_path}", "error")
        except json.JSONDecodeError:
            self.show_notification(f"Invalid JSON: {file_path}", "error")
    
    def load_file(self, event=None):
        # Este método ya no se usa, se mantiene por compatibilidad
        # El sistema ahora usa load_specific_file directamente
        if self.current_file:
            self.load_specific_file(self.current_file)
    
    def refresh_file(self):
        if self.current_file:
            self.load_specific_file(self.current_file)
    
    def update_visual_view(self):
        # Limpiar canvas
        self.visual_canvas.delete('all')
        self.visual_elements = []
        
        if not self.current_data:
            return
        
        # Determinar tipo de archivo y crear vista específica
        if self.current_file == 'posts.json':
            self.create_posts_view()
        elif self.current_file == 'projects.json':
            self.create_projects_view()
        elif self.current_file == 'certifications.json':
            self.create_certifications_view()
        elif self.current_file == 'services.json':
            self.create_services_view()
        elif self.current_file == 'secondary-projects.json':
            self.create_secondary_projects_view()
        elif self.current_file == 'ideas.json':
            self.create_ideas_view()
    
    def create_posts_view(self):
        y_pos = 5
        x_pos = 5
        card_width = 250
        card_height = 150
        gap = 5
        
        for idx, post in enumerate(self.current_data):
            if idx > 0 and idx % 5 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background estilo terminal
            card = self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill=self.colors['bg_card'], outline=self.colors['border'], width=1,
                tags=('card', f'post_{idx}')
            )
            
            # Title estilo terminal
            title = post.get('title', 'Sin título')
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 5,
                text=title[:30] + '...' if len(title) > 30 else title,
                font=self.terminal_font_bold,
                fill=self.colors['text_primary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'post_{idx}')
            )
            
            # Category badge estilo terminal
            category = post.get('category', '') or ''
            if category:
                badge_width = len(category) * 6 + 10
                self.visual_canvas.create_rectangle(
                    x_pos + 5, y_pos + 25, x_pos + 5 + badge_width, y_pos + 40,
                    fill=self.colors['accent'], outline=self.colors['accent'],
                    tags=('card', f'post_{idx}')
                )
                self.visual_canvas.create_text(
                    x_pos + 8, y_pos + 27,
                    text=category.upper()[:8],
                    font=self.terminal_font_small,
                    fill='#000000', anchor='nw',
                    tags=('card', f'post_{idx}')
                )
            
            # Description estilo terminal
            desc = post.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 50,
                text=desc[:60] + '...' if len(desc) > 60 else desc,
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'post_{idx}')
            )
            
            # Date estilo terminal
            date = post.get('createdAt', '')
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + card_height - 15,
                text=date[:10] if date else '',
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'post_{idx}')
            )
            
            # Featured indicator estilo terminal
            if post.get('featured', False):
                self.visual_canvas.create_text(
                    x_pos + card_width - 15, y_pos + 5,
                    text="*",
                    font=self.terminal_font_bold,
                    fill=self.colors['warning'], anchor='ne',
                    tags=('card', f'post_{idx}')
                )
            
            self.visual_elements.append({'type': 'post', 'index': idx, 'data': post, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        # Update scroll region
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_projects_view(self):
        y_pos = 5
        x_pos = 5
        card_width = 220
        card_height = 130
        gap = 5
        
        for idx, project in enumerate(self.current_data):
            if idx > 0 and idx % 6 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background estilo terminal con color personalizado
            color = project.get('color', self.colors['accent'])
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill=self.colors['bg_card'], outline=color, width=1,
                tags=('card', f'project_{idx}')
            )
            
            # Title estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 5,
                text=project.get('title', 'Sin título')[:25] + '...' if len(project.get('title', '')) > 25 else project.get('title', 'Sin título'),
                font=self.terminal_font_bold,
                fill=self.colors['text_primary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'project_{idx}')
            )
            
            # Description estilo terminal
            desc = project.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 30,
                text=desc[:50] + '...' if len(desc) > 50 else desc,
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'project_{idx}')
            )
            
            # Tags estilo terminal
            tags = project.get('tags', [])
            if tags:
                tags_text = ', '.join(tags[:3])
                self.visual_canvas.create_text(
                    x_pos + 5, y_pos + card_height - 20,
                    text=tags_text[:30] + '...' if len(tags_text) > 30 else tags_text,
                    font=self.terminal_font_small,
                    fill=color, anchor='nw',
                    width=card_width - 10,
                    tags=('card', f'project_{idx}')
                )
            
            self.visual_elements.append({'type': 'project', 'index': idx, 'data': project, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def _show_cert_fallback(self, x_pos, y_pos, card_width, cert, idx):
        """Mostrar fallback con primera letra del issuer"""
        issuer = cert.get('issuer', '')
        first_letter = issuer[0].upper() if issuer else '?'
        self.visual_canvas.create_oval(
            x_pos + card_width - 55, y_pos + 10,
            x_pos + card_width - 25, y_pos + 40,
            fill=self.colors['bg_card'], outline=self.colors['accent'], width=2,
            tags=('card', f'cert_{idx}')
        )
        self.visual_canvas.create_text(
            x_pos + card_width - 40, y_pos + 25,
            text=first_letter,
            font=('SF Pro Display', 16, 'bold'),
            fill=self.colors['accent'],
            tags=('card', f'cert_{idx}')
        )
    
    def create_certifications_view(self):
        y_pos = 5
        x_pos = 5
        card_width = 240
        card_height = 100
        gap = 5
        
        for idx, cert in enumerate(self.current_data):
            if idx > 0 and idx % 5 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background estilo terminal
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill=self.colors['bg_card'], outline=self.colors['border'], width=1,
                tags=('card', f'cert_{idx}')
            )
            
            # Icono o badge
            badge_url = cert.get('badge', '')
            icon_name = cert.get('icon', '')
            
            if badge_url:
                # Si hay badge, mostrar texto indicando que hay badge
                self.visual_canvas.create_text(
                    x_pos + card_width - 40, y_pos + 20,
                    text="🏆",
                    font=('SF Pro Display', 24),
                    fill=self.colors['warning'],
                    tags=('card', f'cert_{idx}')
                )
            elif icon_name:
                # Intentar cargar imagen del icono (SVG o PNG)
                svg_path = self.public_path / 'certifications' / f'{icon_name}.svg'
                png_path = self.public_path / 'certifications' / f'{icon_name}.png'
                
                # Primero intentar con SVG usando rsvg-convert (disponible en Arch)
                if svg_path.exists():
                    try:
                        import subprocess
                        import tempfile
                        import os
                        
                        # Crear archivo temporal
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            tmp_path = tmp_file.name
                        
                        # Usar rsvg-convert para convertir SVG a PNG
                        subprocess.run(['rsvg-convert', '-w', '50', '-h', '50', '-o', tmp_path, str(svg_path)], 
                                     check=True, capture_output=True)
                        
                        # Cargar el PNG convertido
                        img = Image.open(tmp_path)
                        photo = ImageTk.PhotoImage(img)
                        
                        # Guardar referencia
                        self.cert_images[f'cert_{idx}'] = photo
                        
                        # Mostrar imagen
                        self.visual_canvas.create_image(
                            x_pos + card_width - 40, y_pos + 25,
                            image=photo,
                            tags=('card', f'cert_{idx}')
                        )
                        
                        # Limpiar archivo temporal
                        os.unlink(tmp_path)
                        
                    except Exception as e:
                        # Si falla rsvg-convert, intentar con cairosvg
                        try:
                            import cairosvg
                            import io
                            svg_data = svg_path.read_text()
                            png_data = cairosvg.svg2png(bytestring=svg_data.encode(), output_width=50, output_height=50)
                            img = Image.open(io.BytesIO(png_data))
                            photo = ImageTk.PhotoImage(img)
                            
                            self.cert_images[f'cert_{idx}'] = photo
                            
                            self.visual_canvas.create_image(
                                x_pos + card_width - 40, y_pos + 25,
                                image=photo,
                                tags=('card', f'cert_{idx}')
                            )
                        except:
                            # Si falla todo, intentar con PNG directo
                            if png_path.exists():
                                try:
                                    img = Image.open(png_path)
                                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                                    photo = ImageTk.PhotoImage(img)
                                    
                                    self.cert_images[f'cert_{idx}'] = photo
                                    
                                    self.visual_canvas.create_image(
                                        x_pos + card_width - 40, y_pos + 25,
                                        image=photo,
                                        tags=('card', f'cert_{idx}')
                                    )
                                except:
                                    # Fallback a primera letra
                                    self._show_cert_fallback(x_pos, y_pos, card_width, cert, idx)
                            else:
                                self._show_cert_fallback(x_pos, y_pos, card_width, cert, idx)
                elif png_path.exists():
                    # Si no hay SVG pero sí PNG
                    try:
                        img = Image.open(png_path)
                        img = img.resize((50, 50), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        self.cert_images[f'cert_{idx}'] = photo
                        
                        self.visual_canvas.create_image(
                            x_pos + card_width - 40, y_pos + 25,
                            image=photo,
                            tags=('card', f'cert_{idx}')
                        )
                    except:
                        self._show_cert_fallback(x_pos, y_pos, card_width, cert, idx)
                else:
                    self._show_cert_fallback(x_pos, y_pos, card_width, cert, idx)
            
            # Name estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 5,
                text=cert.get('name', 'Sin nombre')[:25] + '...' if len(cert.get('name', '')) > 25 else cert.get('name', 'Sin nombre'),
                font=self.terminal_font_bold,
                fill=self.colors['text_primary'], anchor='nw',
                width=card_width - 60,
                tags=('card', f'cert_{idx}')
            )
            
            # Issuer estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 30,
                text=f"{cert.get('issuer', '')[:20]}",
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 60,
                tags=('card', f'cert_{idx}')
            )
            
            # Date estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + card_height - 25,
                text=f"{cert.get('date', '')}",
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'cert_{idx}')
            )
            
            # Credential ID estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + card_height - 12,
                text=f"ID: {cert.get('credentialId', '')[:15]}..." if len(cert.get('credentialId', '')) > 15 else f"ID: {cert.get('credentialId', '')}",
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'cert_{idx}')
            )
            
            self.visual_elements.append({'type': 'cert', 'index': idx, 'data': cert, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_ideas_view(self):
        y_pos = 5
        x_pos = 5
        card_width = 300
        card_height = 80
        gap = 5
        
        for idx, idea in enumerate(self.current_data):
            if idx > 0 and idx % 4 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background estilo terminal
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill=self.colors['bg_card'], outline=self.colors['border'], width=1,
                tags=('card', f'idea_{idx}')
            )
            
            # Content (truncated) estilo terminal
            content = idea.get('content', '')
            if content:
                truncated = content[:80] + '...' if len(content) > 80 else content
                self.visual_canvas.create_text(
                    x_pos + 5, y_pos + 5,
                    text=truncated,
                    font=self.terminal_font,
                    fill=self.colors['text_primary'], anchor='nw',
                    width=card_width - 10,
                    tags=('card', f'idea_{idx}')
                )
            else:
                self.visual_canvas.create_text(
                    x_pos + 5, y_pos + 5,
                    text="[EMPTY]",
                    font=self.terminal_font,
                    fill=self.colors['text_secondary'], anchor='nw',
                    tags=('card', f'idea_{idx}')
                )
            
            # Index indicator estilo terminal
            self.visual_canvas.create_text(
                x_pos + card_width - 10, y_pos + card_height - 10,
                text=f"#{idx + 1}",
                font=self.terminal_font_bold,
                fill=self.colors['accent'], anchor='se',
                tags=('card', f'idea_{idx}')
            )
            
            self.visual_elements.append({'type': 'idea', 'index': idx, 'data': idea, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        # Update scroll region
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_services_view(self):
        y_pos = 5
        x_pos = 5
        card_width = 240
        card_height = 100
        gap = 5
        
        for idx, service in enumerate(self.current_data):
            if idx > 0 and idx % 5 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background estilo terminal
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill=self.colors['bg_card'], outline=self.colors['border'], width=1,
                tags=('card', f'service_{idx}')
            )
            
            # Title estilo terminal
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 5,
                text=service.get('title', 'Sin título')[:25] + '...' if len(service.get('title', '')) > 25 else service.get('title', 'Sin título'),
                font=self.terminal_font_bold,
                fill=self.colors['text_primary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'service_{idx}')
            )
            
            # Description estilo terminal
            desc = service.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 5, y_pos + 30,
                text=desc[:50] + '...' if len(desc) > 50 else desc,
                font=self.terminal_font_small,
                fill=self.colors['text_secondary'], anchor='nw',
                width=card_width - 10,
                tags=('card', f'service_{idx}')
            )
            
            # Order indicator estilo terminal
            order = service.get('order', 0)
            self.visual_canvas.create_text(
                x_pos + card_width - 10, y_pos + card_height - 10,
                text=f"#{order}",
                font=self.terminal_font_bold,
                fill=self.colors['accent'], anchor='se',
                tags=('card', f'service_{idx}')
            )
            
            self.visual_elements.append({'type': 'service', 'index': idx, 'data': service, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_secondary_projects_view(self):
        y_pos = 5
        x_pos = 5
        
        for category, projects in self.current_data.items():
            if isinstance(projects, list):
                # Category header estilo terminal
                self.visual_canvas.create_rectangle(
                    x_pos, y_pos, x_pos + 150, y_pos + 20,
                    fill=self.colors['accent'], outline=self.colors['accent'],
                    tags=('header', f'cat_{category}')
                )
                self.visual_canvas.create_text(
                    x_pos + 5, y_pos + 3,
                    text=category.upper()[:15],
                    font=self.terminal_font_bold,
                    fill='#000000', anchor='nw',
                    tags=('header', f'cat_{category}')
                )
                y_pos += 25
                
                # Projects in category
                card_width = 220
                card_height = 90
                gap = 5
                
                for idx, project in enumerate(projects):
                    if idx > 0 and idx % 5 == 0:
                        x_pos = 20
                        y_pos += card_height + gap
                    
                    # Card background estilo terminal
                    self.visual_canvas.create_rectangle(
                        x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                        fill=self.colors['bg_card'], outline=self.colors['border'], width=1,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Name estilo terminal
                    self.visual_canvas.create_text(
                        x_pos + 5, y_pos + 5,
                        text=project.get('name', 'Sin nombre')[:20] + '...' if len(project.get('name', '')) > 20 else project.get('name', 'Sin nombre'),
                        font=self.terminal_font_bold,
                        fill=self.colors['text_primary'], anchor='nw',
                        width=card_width - 10,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Description estilo terminal
                    desc = project.get('description', '')
                    self.visual_canvas.create_text(
                        x_pos + 5, y_pos + 25,
                        text=desc[:40] + '...' if len(desc) > 40 else desc,
                        font=self.terminal_font_small,
                        fill=self.colors['text_secondary'], anchor='nw',
                        width=card_width - 10,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Tech estilo terminal
                    tech = project.get('tech', [])
                    if tech:
                        tech_text = ', '.join(tech[:2])
                        self.visual_canvas.create_text(
                            x_pos + 5, y_pos + card_height - 20,
                            text=tech_text[:25] + '...' if len(tech_text) > 25 else tech_text,
                            font=self.terminal_font_small,
                            fill=self.colors['accent'], anchor='nw',
                            width=card_width - 10,
                            tags=('card', f'secproj_{category}_{idx}')
                        )
                    
                    x_pos += card_width + gap
                
                x_pos = 20
                y_pos += card_height + gap + 20
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def update_text_editor(self):
        self.text_editor.delete(1.0, tk.END)
        if self.current_data:
            json_str = json.dumps(self.current_data, indent=2, ensure_ascii=False)
            self.text_editor.insert(1.0, json_str)
    
    def on_canvas_click(self, event):
        # Encontrar elemento clickeado
        x, y = event.x, event.y
        clicked_items = self.visual_canvas.find_overlapping(x, y, x+1, y+1)
        
        if clicked_items:
            # Obtener tags del elemento clickeado
            tags = self.visual_canvas.gettags(clicked_items[0])
            if 'card' in tags:
                # Extraer índice y categoría del elemento
                for tag in tags:
                    if tag.startswith('secproj_'):
                        # Formato: secproj_category_idx
                        parts = tag.split('_')
                        if len(parts) >= 3:
                            try:
                                category = parts[1]
                                idx = int(parts[2])
                                # Encontrar el elemento correspondiente en la estructura anidada
                                if isinstance(self.current_data, dict) and category in self.current_data:
                                    projects = self.current_data[category]
                                    if isinstance(projects, list) and idx < len(projects):
                                        element_data = projects[idx]
                                        self.selected_element = {
                                            'type': 'secproj',
                                            'index': idx,
                                            'category': category,
                                            'data': element_data,
                                            'x': 0,  # No se usa para highlight
                                            'y': 0,
                                            'width': 0,
                                            'height': 0
                                        }
                                        self.highlight_selected_from_tags(clicked_items[0])
                                        break
                            except (ValueError, IndexError):
                                pass
                    elif '_' in tag and not tag.startswith('secproj_'):
                        # Para otros tipos (post, project, cert, service)
                        parts = tag.split('_')
                        if len(parts) >= 2:
                            try:
                                idx = int(parts[-1])
                                # Encontrar el elemento correspondiente
                                for element in self.visual_elements:
                                    if element['index'] == idx:
                                        self.selected_element = element
                                        self.highlight_selected(element)
                                        break
                            except ValueError:
                                pass
    
    def on_canvas_double_click(self, event):
        # Encontrar elemento clickeado
        x, y = event.x, event.y
        clicked_items = self.visual_canvas.find_overlapping(x, y, x+1, y+1)
        
        if clicked_items:
            # Obtener tags del elemento clickeado
            tags = self.visual_canvas.gettags(clicked_items[0])
            if 'card' in tags:
                # Extraer índice y categoría del elemento
                for tag in tags:
                    if tag.startswith('secproj_'):
                        # Formato: secproj_category_idx
                        parts = tag.split('_')
                        if len(parts) >= 3:
                            try:
                                category = parts[1]
                                idx = int(parts[2])
                                # Encontrar el elemento correspondiente en la estructura anidada
                                if isinstance(self.current_data, dict) and category in self.current_data:
                                    projects = self.current_data[category]
                                    if isinstance(projects, list) and idx < len(projects):
                                        element_data = projects[idx]
                                        self.selected_element = {
                                            'type': 'secproj',
                                            'index': idx,
                                            'category': category,
                                            'data': element_data,
                                            'x': 0,
                                            'y': 0,
                                            'width': 0,
                                            'height': 0
                                        }
                                        self.edit_element()
                                        break
                            except (ValueError, IndexError):
                                pass
                    elif '_' in tag and not tag.startswith('secproj_'):
                        # Para otros tipos (post, project, cert, service, idea)
                        parts = tag.split('_')
                        if len(parts) >= 2:
                            try:
                                idx = int(parts[-1])
                                # Encontrar el elemento correspondiente
                                for element in self.visual_elements:
                                    if element['index'] == idx:
                                        self.selected_element = element
                                        self.edit_element()
                                        break
                            except ValueError:
                                pass
    
    def highlight_selected(self, element):
        # Remover highlight anterior
        self.visual_canvas.delete('highlight')
        
        # Añadir highlight al elemento seleccionado
        x, y = element['x'], element['y']
        width, height = element['width'], element['height']
        
        self.visual_canvas.create_rectangle(
            x - 2, y - 2, x + width + 2, y + height + 2,
            outline=self.colors['accent'], width=2,
            tags='highlight'
        )
    
    def highlight_selected_from_tags(self, canvas_item):
        # Remover highlight anterior
        self.visual_canvas.delete('highlight')
        
        # Obtener bounding box del item
        bbox = self.visual_canvas.bbox(canvas_item)
        if bbox:
            x1, y1, x2, y2 = bbox
            self.visual_canvas.create_rectangle(
                x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                outline=self.colors['accent'], width=2,
                tags='highlight'
            )
    
    def on_double_click(self, event):
        self.edit_element()
    
    def add_element(self):
        # Si no hay archivo cargado, cargar ideas.json por defecto
        if not self.current_file:
            self.load_specific_file('ideas.json')
        
        # Si después de cargar no hay datos, inicializar como array vacío
        if not self.current_data:
            self.current_data = []
        
        self.editor_mode = 'add'
        self.editor_element = None
        self.populate_editor()
        self.notebook.select(3)  # Ir a la pestaña EDITOR
    
    def edit_element(self):
        if not self.current_data:
            self.show_notification("Load a file first", "warning")
            return
        
        if not self.selected_element:
            self.show_notification("Select element to edit (double-click)", "warning")
            return
        
        self.editor_mode = 'edit'
        self.editor_element = self.selected_element
        self.populate_editor(self.selected_element['data'])
        self.notebook.select(3)  # Ir a la pestaña EDITOR
    
    def delete_element(self):
        if not self.current_data:
            self.show_notification("Load a file first", "warning")
            return
        
        if not self.selected_element:
            self.show_notification("Select element to delete", "warning")
            return
        
        # Eliminar directamente sin confirmación (estilo terminal)
        element = self.selected_element
        
        # Manejar estructura anidada de secondary-projects
        if element.get('type') == 'secproj':
            category = element['category']
            index = element['index']
            
            if isinstance(self.current_data, dict) and category in self.current_data:
                projects = self.current_data[category]
                if isinstance(projects, list) and index < len(projects):
                    try:
                        del self.current_data[category][index]
                        self.update_visual_view()
                        self.update_text_editor()
                        self.mark_unsaved()
                        self.save_file()
                        self.show_notification("Element deleted", "success")
                        self.selected_element = None
                        self.visual_canvas.delete('highlight')
                    except (ValueError, IndexError):
                        self.show_notification("Could not delete element", "error")
            return
        
        # Manejar estructura normal (list)
        index = element['index']
        
        if isinstance(self.current_data, list):
            try:
                del self.current_data[index]
                self.update_visual_view()
                self.update_text_editor()
                self.mark_unsaved()
                self.save_file()
                self.show_notification("Element deleted", "success")
                self.selected_element = None
                self.visual_canvas.delete('highlight')
            except (ValueError, IndexError):
                self.show_notification("Could not delete element", "error")
    
    def save_file(self):
        if not self.current_data or not self.current_file:
            self.show_notification("No data to save", "warning")
            return
        
        # También actualizar desde el editor de texto si está modificado
        try:
            text_content = self.text_editor.get(1.0, tk.END).strip()
            if text_content:
                self.current_data = json.loads(text_content)
        except json.JSONDecodeError:
            pass  # Si hay error, mantener los datos actuales
        
        file_path = self.base_path / self.current_file
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_data, f, indent=2, ensure_ascii=False)
            
            self.unsaved_changes = False
            self.unsaved_label.config(text="")
            self.show_notification(f"Saved: {self.current_file}", "success")
            
            # Hacer git commit y push automáticamente en background
            import threading
            threading.Thread(target=self.git_commit_and_push, daemon=True).start()
            
        except Exception as e:
            self.show_notification(f"Error saving: {str(e)}", "error")
    
    def git_commit_and_push(self):
        """Hacer git commit y push seguro usando las credenciales ya configuradas"""
        try:
            # Verificar si hay cambios (usando cwd en lugar de chdir)
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            if not result.stdout.strip():
                self.show_notification("No changes to commit", "info")
                return
            
            # Agregar solo archivos JSON seguros (excluyendo ideas.json que está en .gitignore)
            json_files_to_add = []
            for json_file in ['posts.json', 'projects.json', 'secondary-projects.json', 
                            'certifications.json', 'services.json']:
                file_path = self.base_path / json_file
                if file_path.exists():
                    json_files_to_add.append(str(file_path))
            
            if json_files_to_add:
                # Agregar archivos específicos
                add_result = subprocess.run(['git', 'add'] + json_files_to_add, 
                                          capture_output=True, text=True, cwd=self.project_root)
                if add_result.returncode != 0:
                    self.show_notification(f"Git add error: {add_result.stderr}", "error")
                    return
                
                # Crear commit con mensaje descriptivo
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                commit_message = f"Update {self.current_file} - {timestamp}"
                commit_result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                             capture_output=True, text=True, cwd=self.project_root)
                if commit_result.returncode != 0:
                    self.show_notification(f"Git commit error: {commit_result.stderr}", "error")
                    return
                
                # Push al remoto
                push_result = subprocess.run(['git', 'push'], 
                                           capture_output=True, text=True, cwd=self.project_root)
                if push_result.returncode != 0:
                    self.show_notification(f"Git push error: {push_result.stderr}", "error")
                    return
                
                self.show_notification("Changes pushed to Git", "success")
            else:
                self.show_notification("No JSON files to commit", "info")
                
        except Exception as e:
            self.show_notification(f"Git error: {str(e)}", "error")
    
    def mark_unsaved(self):
        self.unsaved_changes = True
        self.unsaved_label.config(text="● Unsaved changes")
    
    def animate_title(self):
        """Animación sutil del título"""
        opacities = [1.0, 0.9, 1.0, 0.95]
        self.title_opacity_index = 0
        
        def pulse():
            if hasattr(self, 'title_label'):
                opacity = opacities[self.title_opacity_index]
                # Simular opacidad cambiando el color
                gray_value = int(201 * opacity)
                color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
                self.title_label.config(fg=color)
                self.title_opacity_index = (self.title_opacity_index + 1) % len(opacities)
                self.root.after(800, pulse)
        
        self.root.after(800, pulse)
    
    def animate_neon_border(self):
        """Animación sutil del borde en las tarjetas seleccionadas"""
        self.neon_colors = [self.colors['accent'], '#79c0ff', self.colors['accent'], '#58a6ff']
        self.neon_index = 0
        
        def pulse_neon():
            if hasattr(self, 'visual_canvas') and self.selected_element:
                self.visual_canvas.delete('neon_highlight')
                color = self.neon_colors[self.neon_index]
                
                element = self.selected_element
                x, y = element['x'], element['y']
                width, height = element['width'], element['height']
                
                self.visual_canvas.create_rectangle(
                    x - 3, y - 3, x + width + 3, y + height + 3,
                    outline=color, width=2,
                    tags='neon_highlight'
                )
                
                self.neon_index = (self.neon_index + 1) % len(self.neon_colors)
                self.root.after(400, pulse_neon)
        
        self.root.after(400, pulse_neon)
    
    def animate_status_bar(self):
        """Animación de la barra de estado con mensajes cíclicos"""
        messages = [
            "Ready — System online",
            "Blanch.cc JSON Editor",
            "Press ESC to exit fullscreen",
            "Double-click to edit elements"
        ]
        self.message_index = 0
        
        def cycle_messages():
            if hasattr(self, 'status_var') and not self.current_file:
                message = messages[self.message_index]
                self.status_var.set(message)
                self.message_index = (self.message_index + 1) % len(messages)
                self.root.after(4000, cycle_messages)
        
        self.root.after(4000, cycle_messages)
    
    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado mejorados estilo terminal"""
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-r>', lambda e: self.refresh_file())
        self.root.bind('<Control-n>', lambda e: self.add_element())
        self.root.bind('<Delete>', lambda e: self.delete_element())
        self.root.bind('<F5>', lambda e: self.refresh_file())
        self.root.bind('<F2>', lambda e: self.edit_element())
        self.root.bind('<Escape>', lambda e: self.cancel_editor())
        
        # Atajos para navegación de pestañas
        self.root.bind('<Control-1>', lambda e: self.notebook.select(0))
        self.root.bind('<Control-2>', lambda e: self.notebook.select(1))
        self.root.bind('<Control-3>', lambda e: self.notebook.select(2))
        self.root.bind('<Control-4>', lambda e: self.notebook.select(3))
        
        # Atajos para archivos específicos
        self.root.bind('<Alt-c>', lambda e: self.load_specific_file('certifications.json'))
        self.root.bind('<Alt-p>', lambda e: self.load_specific_file('posts.json'))
        self.root.bind('<Alt-j>', lambda e: self.load_specific_file('projects.json'))
        self.root.bind('<Alt-s>', lambda e: self.load_specific_file('secondary-projects.json'))
        self.root.bind('<Alt-v>', lambda e: self.load_specific_file('services.json'))
        self.root.bind('<Alt-i>', lambda e: self.load_specific_file('ideas.json'))
    
    def on_canvas_hover(self, event):
        """Efecto hover al pasar el mouse sobre tarjetas"""
        x, y = event.x, event.y
        hovered_items = self.visual_canvas.find_overlapping(x, y, x+1, y+1)
        
        # Eliminar hover effect anterior
        self.visual_canvas.delete('hover_effect')
        
        if hovered_items:
            tags = self.visual_canvas.gettags(hovered_items[0])
            if 'card' in tags:
                # Encontrar el elemento correspondiente
                for tag in tags:
                    if '_' in tag:
                        parts = tag.split('_')
                        if len(parts) >= 2:
                            try:
                                idx = int(parts[-1])
                                for element in self.visual_elements:
                                    if element['index'] == idx and element != self.selected_element:
                                        # Añadir efecto hover
                                        elem_x, elem_y = element['x'], element['y']
                                        elem_width, elem_height = element['width'], element['height']
                                        
                                        self.visual_canvas.create_rectangle(
                                            elem_x - 1, elem_y - 1, 
                                            elem_x + elem_width + 1, elem_y + elem_height + 1,
                                            outline='#ff6666', width=1,
                                            tags='hover_effect'
                                        )
                                        break
                            except ValueError:
                                pass
    
    def populate_editor(self, element=None):
        # Limpiar el editor
        for widget in self.editor_scrollable_frame.winfo_children():
            if widget != self.editor_button_frame:
                widget.destroy()
        
        self.editor_entries = {}
        
        # Campos según el tipo de archivo
        fields = self.get_fields_for_file_type()
        
        # Obtener categorías y series existentes para posts
        existing_categories = set()
        existing_series = set()
        if self.current_file == 'posts.json' and isinstance(self.current_data, list):
            for post in self.current_data:
                if 'category' in post:
                    existing_categories.add(post['category'])
                if 'series' in post and post['series']:
                    existing_series.add(post['series'])
        
        # Categorías y niveles técnicos para ideas
        idea_categories = ['Development', 'Design', 'Tutorial', 'Case Study', 'Opinion']
        tech_levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        
        # Crear frame para 2 columnas - compacto
        columns_frame = tk.Frame(self.editor_scrollable_frame, bg=self.colors['bg'])
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
        
        # Frame para columna izquierda
        left_column = tk.Frame(columns_frame, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        
        # Frame para columna derecha
        right_column = tk.Frame(columns_frame, bg=self.colors['bg'])
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(3, 0))
        
        for idx, (field, field_type) in enumerate(fields.items()):
            # Para campos grandes (markdown, content), usar todo el ancho
            if field in ['content', 'markdown']:
                column = columns_frame
            else:
                # Alternar entre columnas
                column = left_column if idx % 2 == 0 else right_column
            
            frame = tk.Frame(column, bg=self.colors['bg'])
            frame.pack(fill=tk.X, pady=3)
            
            label = tk.Label(frame, text=f"[{field.upper()}]:", font=self.terminal_font_bold, 
                           bg=self.colors['bg'], fg=self.colors['text_primary'])
            label.pack(anchor=tk.W)
            
            if field_type == 'text' or field_type == 'readonly':
                state = 'readonly' if field_type == 'readonly' else 'normal'
                bg_color = self.colors['bg_hover'] if field_type == 'readonly' else self.colors['bg_card']
                entry = tk.Entry(frame, width=50, bg=bg_color, fg=self.colors['text_secondary'], 
                               insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1, state=state)
                entry.pack(fill=tk.X, ipady=2)
            elif field_type == 'textarea':
                # Para ideas.json, hacer el textarea más grande
                textarea_height = 20 if self.current_file == 'ideas.json' else 6
                entry = tk.Text(frame, height=textarea_height, width=50, bg=self.colors['bg_card'], fg=self.colors['text_primary'], 
                              insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
                entry.pack(fill=tk.X)
            elif field_type == 'markdown':
                entry = tk.Text(frame, height=20, width=80, bg=self.colors['bg_card'], fg=self.colors['text_primary'], 
                              insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
                entry.pack(fill=tk.BOTH, expand=True)
            elif field_type == 'number':
                entry = tk.Entry(frame, width=50, bg=self.colors['bg_card'], fg=self.colors['text_primary'], 
                               insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
                entry.pack(fill=tk.X, ipady=2)
            elif field_type == 'readonly_number':
                entry = tk.Entry(frame, width=50, bg=self.colors['bg_hover'], fg=self.colors['text_secondary'], 
                               insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1, state='readonly')
                entry.pack(fill=tk.X, ipady=2)
            elif field_type == 'color':
                entry = tk.Entry(frame, width=50, bg=self.colors['bg_card'], fg=self.colors['text_primary'], 
                               insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
                entry.pack(fill=tk.X, ipady=2)
            elif field_type == 'array':
                entry = tk.Text(frame, height=2, width=50, bg=self.colors['bg_card'], fg=self.colors['text_primary'], 
                              insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
                entry.pack(fill=tk.X)
            elif field_type == 'boolean':
                # Inicializar con el valor del elemento si estamos editando
                default_value = 'false'
                if element and field in element:
                    default_value = 'true' if element[field] else 'false'
                var = tk.StringVar(value=default_value)
                entry = ttk.Combobox(frame, textvariable=var, values=['true', 'false'], 
                                   state='readonly', width=47, font=self.terminal_font)
                entry.pack(fill=tk.X, ipady=2)
                self.editor_entries[field] = (var, 'boolean')
                continue
            elif field_type == 'select':
                var = tk.StringVar()
                # Para ideas.json, usar categorías predefinidas
                if self.current_file == 'ideas.json' and field == 'category':
                    values = idea_categories + ['']
                else:
                    values = ['[Create new...]'] + list(existing_categories) + [''] if existing_categories else ['[Create new...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=self.terminal_font)
                entry.pack(fill=tk.X, ipady=2)
                if self.current_file != 'ideas.json':
                    entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_category_selected(f, v))
                self.editor_entries[field] = (var, 'select')
                continue
            elif field_type == 'select_series':
                var = tk.StringVar()
                values = ['[Create new...]'] + list(existing_series) + [''] if existing_series else ['[Create new...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=self.terminal_font)
                entry.pack(fill=tk.X, ipady=2)
                entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_series_selected(f, v))
                self.editor_entries[field] = (var, 'select_series')
                continue
            elif field_type == 'select' and field == 'technical_level':
                var = tk.StringVar(value='Intermediate')
                entry = ttk.Combobox(frame, textvariable=var, values=tech_levels, 
                                   state='readonly', width=47, font=self.terminal_font)
                entry.pack(fill=tk.X, ipady=2)
                self.editor_entries[field] = (var, 'select')
                continue
            elif field_type == 'select_post':
                var = tk.StringVar()
                posts_list = self.get_existing_posts()
                values = ['[SIN POST ASOCIADO]'] + posts_list + [''] if posts_list else ['[SIN POST ASOCIADO]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=self.terminal_font)
                entry.pack(fill=tk.X, ipady=2)
                self.editor_entries[field] = (var, 'select_post')
                continue
            elif field_type == 'select_posts_multiple':
                posts_list = self.get_existing_posts()
                if posts_list:
                    # Frame para checkboxes
                    checkbox_frame = tk.Frame(frame, bg=self.colors['bg'])
                    checkbox_frame.pack(fill=tk.X, pady=2)
                    
                    checkbox_container = tk.Frame(checkbox_frame, bg=self.colors['bg'])
                    checkbox_container.pack(fill=tk.BOTH, expand=True)
                    
                    # Crear checkboxes para cada post
                    checkboxes = {}
                    for idx, post in enumerate(posts_list):
                        # Extraer ID del formato "Título | ID"
                        post_id = post.split(' | ')[-1].strip() if ' | ' in post else post
                        var = tk.BooleanVar()
                        cb = tk.Checkbutton(checkbox_container, text=post[:30] + '...' if len(post) > 30 else post, variable=var,
                                          bg=self.colors['bg'], fg=self.colors['text_primary'],
                                          font=self.terminal_font_small, selectcolor=self.colors['accent'],
                                          activebackground=self.colors['bg'], activeforeground=self.colors['accent'],
                                          relief=tk.FLAT, bd=1, anchor='w')
                        cb.pack(fill=tk.X, padx=2, pady=1)
                        checkboxes[post_id] = var
                    
                    self.editor_entries[field] = (checkboxes, 'select_posts_multiple')
                else:
                    tk.Label(frame, text="[NO POSTS]", font=self.terminal_font_small,
                           bg=self.colors['bg'], fg=self.colors['text_secondary']).pack()
                    self.editor_entries[field] = (None, 'select_posts_multiple')
                continue
            
            # Valor por defecto si estamos editando
            if element and field in element:
                value = element[field]
                if field_type in ['textarea', 'array', 'markdown']:
                    if isinstance(value, list):
                        entry.insert(1.0, ', '.join(str(v) for v in value))
                    else:
                        entry.insert(1.0, str(value))
                else:
                    entry.insert(0, str(value))
            
            self.editor_entries[field] = (entry, field_type)
        
        # Manejar selección de post para certificaciones
        if element and 'relatedPostId' in element and element['relatedPostId']:
            if 'relatedPostId' in self.editor_entries:
                var, field_type = self.editor_entries['relatedPostId']
                if var and field_type == 'select_post':
                    # Buscar el post en la lista y seleccionarlo
                    posts_list = self.get_existing_posts()
                    post_id = element['relatedPostId']
                    for post in posts_list:
                        if post_id in post:
                            var.set(post)
                            break
                    if not var.get():
                        var.set('[SIN POST ASOCIADO]')
        
        # Manejar selección múltiple de posts para edición
        if element and 'relatedPostIds' in element and element['relatedPostIds']:
            if 'relatedPostIds' in self.editor_entries:
                checkboxes, field_type = self.editor_entries['relatedPostIds']
                if checkboxes and field_type == 'select_posts_multiple':
                    # Marcar los checkboxes de los posts que ya están asociados
                    for post_id, var in checkboxes.items():
                        if post_id in element['relatedPostIds']:
                            var.set(True)
        
        # Categoría para secondary-projects
        if self.current_file == 'secondary-projects.json' and not element:
            cat_frame = tk.Frame(self.editor_scrollable_frame, bg=self.colors['bg'])
            cat_frame.pack(fill=tk.X, padx=5, pady=3)
            
            tk.Label(cat_frame, text="[CATEGORY]:", font=self.terminal_font_bold, 
                   bg=self.colors['bg'], fg=self.colors['text_primary']).pack(anchor=tk.W)
            
            categories = list(self.current_data.keys()) if isinstance(self.current_data, dict) else []
            cat_var = tk.StringVar()
            cat_values = ['[Create new...]'] + categories if categories else ['[Create new...]']
            cat_combo = ttk.Combobox(cat_frame, textvariable=cat_var, values=cat_values, 
                                   state='readonly', width=47, font=self.terminal_font)
            cat_combo.pack(fill=tk.X, ipady=2)
            cat_combo.bind('<<ComboboxSelected>>', lambda e, v=cat_var: self.on_category_selected_secondary(v))
            self.editor_entries['category'] = (cat_var, 'select')
        
        # Mover los botones al final
        self.editor_button_frame.pack_forget()
        self.editor_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Actualizar scroll region
        self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))
    
    def on_category_selected(self, field, var):
        if var.get() == '[Create new...]':
            new_category = simpledialog.askstring("New Category", "Enter the new category name:")
            if new_category:
                var.set(new_category)
    
    def on_series_selected(self, field, var):
        if var.get() == '[Create new...]':
            new_series = simpledialog.askstring("New Series", "Enter the new series name:")
            if new_series:
                var.set(new_series)
    
    def on_category_selected_secondary(self, var):
        if var.get() == '[Create new...]':
            new_category = simpledialog.askstring("New Category", "Enter the new category name:")
            if new_category:
                var.set(new_category)
                # Crear la nueva categoría en el JSON si no existe
                if isinstance(self.current_data, dict) and new_category not in self.current_data:
                    self.current_data[new_category] = []
                    self.mark_unsaved()

    def get_existing_posts(self):
        """Obtener lista de todos los posts para el selector"""
        posts_list = []
        try:
            posts_path = self.base_path / 'posts.json'
            if posts_path.exists():
                with open(posts_path, 'r', encoding='utf-8') as f:
                    posts_data = json.load(f)
                    if isinstance(posts_data, list):
                        for post in posts_data:
                            post_id = post.get('id', '')
                            post_title = post.get('title', 'Sin título')
                            # Formato simple: Título | ID
                            posts_list.append(f"{post_title} | {post_id}")
        except Exception as e:
            print(f"Error loading posts: {e}")
        return posts_list
    
    def get_fields_for_file_type(self):
        # Cargar posts existentes para el selector
        existing_posts = []
        try:
            posts_path = self.base_path / 'posts.json'
            if posts_path.exists():
                with open(posts_path, 'r', encoding='utf-8') as f:
                    posts_data = json.load(f)
                    if isinstance(posts_data, list):
                        existing_posts = [f"{p.get('title', 'Sin título')} ({p.get('id', '')})" for p in posts_data if p.get('published', True)]
        except:
            pass

        if self.current_file == 'certifications.json':
            return {
                'id': 'text',
                'name': 'text',
                'icon': 'text',
                'order': 'number',
                'issuer': 'text',
                'date': 'text',
                'credentialId': 'text',
                'badge': 'text',
                'relatedPostId': 'select_post'
            }
        elif self.current_file == 'posts.json':
            return {
                'id': 'readonly',
                'slug': 'text',
                'title': 'text',
                'category': 'select',
                'description': 'textarea',
                'content': 'markdown',
                'createdAt': 'readonly',
                'keywords': 'array',
                'readingTime': 'readonly',
                'wordCount': 'readonly',
                'featured': 'boolean',
                'published': 'boolean',
                'series': 'select_series',
                'seriesOrder': 'number',
                'seriesPartTitle': 'text'
            }
        elif self.current_file == 'projects.json':
            return {
                'id': 'readonly',
                'title': 'text',
                'description': 'textarea',
                'image': 'text',
                'tags': 'array',
                'color': 'color',
                'order': 'number',
                'relatedPostIds': 'select_posts_multiple'
            }
        elif self.current_file == 'secondary-projects.json':
            return {
                'id': 'readonly',
                'name': 'text',
                'description': 'textarea',
                'details': 'textarea',
                'tech': 'array',
                'link': 'text',
                'relatedPostIds': 'select_posts_multiple'
            }
        elif self.current_file == 'services.json':
            return {
                'id': 'readonly',
                'title': 'text',
                'description': 'textarea',
                'order': 'number'
            }
        elif self.current_file == 'ideas.json':
            return {
                'content': 'textarea'
            }
        return {}
    
    def save_editor(self):
        result = {}
        
        for field, (entry, field_type) in self.editor_entries.items():
            # Saltar campos readonly - mantener el valor original del elemento
            if field_type == 'readonly' and self.editor_element and field in self.editor_element.get('data', {}):
                result[field] = self.editor_element['data'][field]
                continue
            
            if field_type in ['textarea', 'markdown']:
                value = entry.get(1.0, tk.END).strip()
            elif field_type == 'array':
                value = entry.get(1.0, tk.END).strip()
                if value:
                    value = [v.strip() for v in value.split(',')]
                else:
                    value = []
            elif field_type == 'number':
                value = entry.get().strip()
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        value = 0
            elif field_type == 'boolean':
                value = entry.get() == 'true'
            elif field_type in ['select', 'select_series', 'select_post']:
                value = entry.get().strip()
                if not value or value == '[SIN POST ASOCIADO]':
                    value = None
                # Para category, asegurar que no sea None
                if field == 'category' and value is None:
                    value = ''
                # Para relatedPostId, extraer el ID del formato "Título | ID"
                if field == 'relatedPostId' and value and '|' in value:
                    value = value.split('|')[-1].strip()
                # Para select_post, manejar "[No related post]"
                if field == 'relatedPostId' and value == '[No related post]':
                    value = None
            elif field_type == 'select_posts_multiple':
                # Extraer los IDs de los posts seleccionados de los checkboxes
                if entry:
                    post_ids = []
                    for post_id, var in entry.items():
                        if var.get():
                            post_ids.append(post_id)
                    value = post_ids if post_ids else []
                else:
                    value = []
            else:
                value = entry.get().strip()
            
            result[field] = value
        
        # Añadir campo tech vacío para projects si no existe
        if self.current_file == 'projects.json' and 'tech' not in result:
            result['tech'] = []
        
        # Añadir relatedPostIds si no existe (para compatibilidad)
        if self.current_file in ['projects.json', 'secondary-projects.json']:
            if 'relatedPostIds' not in result:
                result['relatedPostIds'] = []
        # Mantener relatedPostId para certificaciones (compatibilidad)
        if self.current_file == 'certifications.json':
            if 'relatedPostId' not in result:
                result['relatedPostId'] = None
        
        # Para posts, asegurar que los campos nuevos tengan valores por defecto
        if self.current_file == 'posts.json':
            if 'keywords' not in result or not result['keywords']:
                result['keywords'] = []
            if 'featured' not in result:
                result['featured'] = False
            if 'published' not in result:
                result['published'] = True
            if 'series' not in result or not result['series']:
                result['series'] = None
            if 'seriesOrder' not in result:
                result['seriesOrder'] = None
            if 'seriesPartTitle' not in result:
                result['seriesPartTitle'] = None
            # Auto-generar createdAt si está vacío o no existe
            if 'createdAt' not in result or not result['createdAt']:
                result['createdAt'] = datetime.now().isoformat()
            # Calcular wordCount y readingTime automáticamente desde el contenido
            if 'content' in result and result['content']:
                # Contar palabras (separando por espacios y saltos de línea)
                words = result['content'].split()
                result['wordCount'] = len(words)
                # Calcular tiempo de lectura (200 palabras por minuto)
                result['readingTime'] = max(1, round(len(words) / 200))
            else:
                result['wordCount'] = 0
                result['readingTime'] = 0
        
        # Aplicar cambios según el modo
        if self.editor_mode == 'add':
            if isinstance(self.current_data, list):
                self.current_data.append(result)
            elif isinstance(self.current_data, dict):
                category = result.get('category', '')
                if category in self.current_data and isinstance(self.current_data[category], list):
                    self.current_data[category].append(result)
            self.status_var.set("Elemento añadido")
        elif self.editor_mode == 'edit':
            element = self.editor_element
            if element.get('type') == 'secproj':
                category = element['category']
                index = element['index']
                if isinstance(self.current_data, dict) and category in self.current_data:
                    projects = self.current_data[category]
                    if isinstance(projects, list) and index < len(projects):
                        self.current_data[category][index] = result
            else:
                index = element['index']
                if isinstance(self.current_data, list):
                    self.current_data[index] = result
            self.status_var.set("Elemento actualizado")
        
        self.update_visual_view()
        self.update_text_editor()
        self.mark_unsaved()
        # Guardar automáticamente al archivo
        self.save_file()
        self.cancel_editor()
    
    def cancel_editor(self):
        self.notebook.select(1)  # Volver a la vista visual
        self.editor_mode = None
        self.editor_element = None
    
    def load_ideas(self):
        """Cargar ideas desde el archivo JSON"""
        try:
            if self.ideas_file.exists():
                with open(self.ideas_file, 'r', encoding='utf-8') as f:
                    self.ideas_data = json.load(f)
            else:
                self.ideas_data = []
        except:
            self.ideas_data = []
        
        self.update_ideas_listbox()
    
    def save_ideas_to_file(self):
        """Guardar ideas al archivo JSON"""
        try:
            with open(self.ideas_file, 'w', encoding='utf-8') as f:
                json.dump(self.ideas_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.show_notification(f"Error saving ideas: {str(e)}", "error")
    
    def update_ideas_listbox(self):
        """Actualizar el listbox con las ideas guardadas - estilo terminal"""
        self.ideas_listbox.delete(0, tk.END)
        for idx, idea in enumerate(self.ideas_data):
            content = idea.get('content', '')
            # Mostrar primera línea como título
            lines = content.split('\n')
            first_line = lines[0][:60] + '...' if len(lines[0]) > 60 else lines[0]
            display_text = first_line if first_line else '[empty]'
            self.ideas_listbox.insert(tk.END, display_text)
    
    def new_idea(self):
        """Crear nueva idea"""
        self.current_idea_id = None
        self.idea_content_text.delete(1.0, tk.END)
        self.prompt_text.delete(1.0, tk.END)
        self.ideas_listbox.selection_clear(0, tk.END)
    
    def delete_idea(self):
        """Eliminar idea seleccionada"""
        selection = self.ideas_listbox.curselection()
        if not selection:
            self.show_notification("Select an idea to delete", "warning")
            return
        
        idx = selection[0]
        if idx < len(self.ideas_data):
            del self.ideas_data[idx]
            self.save_ideas_to_file()
            self.update_ideas_listbox()
            self.new_idea()
            self.show_notification("Idea deleted", "success")
    
    def on_idea_selected(self, event):
        """Cuando se selecciona una idea de la lista"""
        # Guardar la idea actual antes de cambiar
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            self.save_idea_silent()
        
        selection = self.ideas_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if idx < len(self.ideas_data):
            idea = self.ideas_data[idx]
            self.current_idea_id = idx
            
            self.idea_content_text.delete(1.0, tk.END)
            content = idea.get('content', '')
            if content:
                self.idea_content_text.insert(1.0, content)
            
            self.prompt_text.delete(1.0, tk.END)
            if idea.get('generated_prompt'):
                self.prompt_text.insert(1.0, idea['generated_prompt'])
    
    def on_idea_key_release(self, event):
        """Auto-save al escribir en el editor de ideas"""
        # Cancelar timer anterior
        if self.idea_autosave_timer:
            self.root.after_cancel(self.idea_autosave_timer)
        
        # Programar auto-save después de 2 segundos
        self.idea_autosave_timer = self.root.after(2000, self.save_idea_silent)
    
    def save_idea_silent(self):
        """Guardar idea sin notificaciones (auto-save)"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        
        if not content:
            return
        
        # Mantener el created_at original si existe
        original_created_at = None
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            original_created_at = self.ideas_data[self.current_idea_id].get('created_at')
        
        idea_data = {
            'content': content,
            'generated_prompt': self.prompt_text.get(1.0, tk.END).strip(),
            'created_at': original_created_at if original_created_at else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            # Actualizar idea existente
            self.ideas_data[self.current_idea_id] = idea_data
        else:
            # Crear nueva idea
            self.ideas_data.append(idea_data)
            self.current_idea_id = len(self.ideas_data) - 1
        
        self.save_ideas_to_file()
        self.update_ideas_listbox()
    
    def save_idea(self):
        """Guardar la idea actual"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        if not content:
            self.show_notification("Content is required", "warning")
            return
        
        idea_data = {
            'content': content,
            'generated_prompt': self.prompt_text.get(1.0, tk.END).strip(),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            # Actualizar idea existente
            self.ideas_data[self.current_idea_id] = idea_data
        else:
            # Crear nueva idea
            self.ideas_data.append(idea_data)
            self.current_idea_id = len(self.ideas_data) - 1
        
        self.save_ideas_to_file()
        self.update_ideas_listbox()
        self.show_notification("Idea saved successfully", "success")
    
    def generate_ai_prompt(self):
        """Generar prompt optimizado para IA"""
        title = self.idea_title_entry.get().strip()
        category = self.idea_category_var.get()
        main_idea = self.idea_main_text.get(1.0, tk.END).strip()
        key_points = self.idea_points_text.get(1.0, tk.END).strip()
        audience = self.idea_audience_entry.get().strip()
        tech_level = self.idea_tech_level_var.get()
        notes = self.idea_notes_text.get(1.0, tk.END).strip()
        
        if not title or not main_idea:
            messagebox.showwarning("Warning", "Title and Main Idea are required")
            return
        
        # Generar prompt estructurado
        prompt = f"""You are an expert technical blog writer specializing in {category.lower()} content. Write a comprehensive blog post with the following specifications:

TITLE: {title}

CATEGORY: {category}

TARGET AUDIENCE: {audience if audience else 'Developers and tech enthusiasts'}

TECHNICAL LEVEL: {tech_level}

MAIN CONCEPT:
{main_idea}

KEY POINTS TO COVER:
{key_points}

ADDITIONAL CONTEXT:
{notes if notes else 'None provided'}

REQUIREMENTS:
1. Write in a professional yet engaging tone suitable for a technical blog
2. Include practical code examples where applicable
3. Structure with clear headings and subheadings
4. Include a compelling introduction and conclusion
5. Add relevant technical keywords for SEO
6. Estimate reading time based on word count
7. Suggest 5-8 relevant keywords/tags
8. Keep paragraphs concise and readable
9. Use markdown formatting for code blocks and emphasis
10. Include a brief description (2-3 sentences) for the post preview

OUTPUT FORMAT:
Please provide the response in the following JSON structure:
{{
  "title": "{title}",
  "slug": "url-friendly-slug",
  "category": "{category}",
  "description": "Brief 2-3 sentence description",
  "content": "Full markdown content with proper formatting",
  "keywords": ["keyword1", "keyword2", ...],
  "readingTime": estimated_minutes,
  "wordCount": estimated_words,
  "featured": false,
  "published": true,
  "createdAt": "{datetime.now().strftime('%Y-%m-%d')}"
}}

Focus on creating content that is technically accurate, well-structured, and valuable to {tech_level.lower()} level developers."""
        
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(1.0, prompt)
        
        # Guardar el prompt en la idea actual
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            self.ideas_data[self.current_idea_id]['generated_prompt'] = prompt
            self.save_ideas_to_file()
    
    def copy_prompt(self):
        """Copiar el prompt"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            self.show_notification("Prompt copied to clipboard", "success")
        else:
            self.show_notification("No prompt to copy", "warning")
    
    def edit_post_data(self):
        """Editar datos específicos para post"""
        if self.current_idea_id is None or self.current_idea_id >= len(self.ideas_data):
            self.show_notification("Select an idea first", "warning")
            return
        
        post_data = self.ideas_data[self.current_idea_id].get('post_data', {})
        
        dialog = tk.Toplevel(self.root)
        dialog.title("[EDIT POST DATA]")
        dialog.geometry("400x450")
        dialog.configure(bg=self.colors['bg'])
        
        entries = {}
        
        # Slug
        tk.Label(dialog, text="[SLUG]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['slug'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['slug'].pack(fill=tk.X, padx=5, pady=2)
        entries['slug'].insert(0, post_data.get('slug', ''))
        
        # Category
        tk.Label(dialog, text="[CATEGORY]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['category'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['category'].pack(fill=tk.X, padx=5, pady=2)
        entries['category'].insert(0, post_data.get('category', 'Development'))
        
        # Description
        tk.Label(dialog, text="[DESCRIPTION]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['description'] = tk.Text(dialog, height=3, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['description'].pack(fill=tk.X, padx=5, pady=2)
        entries['description'].insert(1.0, post_data.get('description', ''))
        
        # Keywords
        tk.Label(dialog, text="[KEYWORDS]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['keywords'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['keywords'].pack(fill=tk.X, padx=5, pady=2)
        entries['keywords'].insert(0, ', '.join(post_data.get('keywords', [])))
        
        # Reading Time
        tk.Label(dialog, text="[READING TIME]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['readingTime'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['readingTime'].pack(fill=tk.X, padx=5, pady=2)
        entries['readingTime'].insert(0, str(post_data.get('readingTime', 5)))
        
        # Featured
        featured_var = tk.BooleanVar(value=post_data.get('featured', False))
        tk.Checkbutton(dialog, text="[FEATURED]", variable=featured_var, bg=self.colors['bg'], fg=self.colors['text_primary'], selectcolor=self.colors['accent'], activebackground=self.colors['bg'], font=self.terminal_font).pack(anchor=tk.W, padx=5, pady=(5, 2))
        
        # Published
        published_var = tk.BooleanVar(value=post_data.get('published', False))
        tk.Checkbutton(dialog, text="[PUBLISHED]", variable=published_var, bg=self.colors['bg'], fg=self.colors['text_primary'], selectcolor=self.colors['accent'], activebackground=self.colors['bg'], font=self.terminal_font).pack(anchor=tk.W, padx=5, pady=(5, 2))
        
        def save_post_data():
            self.ideas_data[self.current_idea_id]['post_data'] = {
                'slug': entries['slug'].get().strip(),
                'category': entries['category'].get().strip(),
                'description': entries['description'].get(1.0, tk.END).strip(),
                'keywords': [k.strip() for k in entries['keywords'].get().split(',') if k.strip()],
                'readingTime': int(entries['readingTime'].get()) if entries['readingTime'].get().isdigit() else 5,
                'featured': featured_var.get(),
                'published': published_var.get()
            }
            self.save_ideas_to_file()
            self.show_notification("Post data saved", "success")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="[S]SAVE", command=save_post_data, bg=self.colors['success'], fg='#000000', font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="[ESC]CANCEL", command=dialog.destroy, bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
    
    def edit_project_data(self):
        """Editar datos específicos para project"""
        if self.current_idea_id is None or self.current_idea_id >= len(self.ideas_data):
            self.show_notification("Select an idea first", "warning")
            return
        
        project_data = self.ideas_data[self.current_idea_id].get('project_data', {})
        
        dialog = tk.Toplevel(self.root)
        dialog.title("[EDIT PROJECT DATA]")
        dialog.geometry("400x350")
        dialog.configure(bg=self.colors['bg'])
        
        entries = {}
        
        # Image
        tk.Label(dialog, text="[IMAGE URL]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['image'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['image'].pack(fill=tk.X, padx=5, pady=2)
        entries['image'].insert(0, project_data.get('image', '/images/default.png'))
        
        # Tags
        tk.Label(dialog, text="[TAGS]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['tags'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['tags'].pack(fill=tk.X, padx=5, pady=2)
        entries['tags'].insert(0, ', '.join(project_data.get('tags', [])))
        
        # Tech
        tk.Label(dialog, text="[TECH STACK]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['tech'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['tech'].pack(fill=tk.X, padx=5, pady=2)
        entries['tech'].insert(0, ', '.join(project_data.get('tech', [])))
        
        # Color
        tk.Label(dialog, text="[COLOR]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['color'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['color'].pack(fill=tk.X, padx=5, pady=2)
        entries['color'].insert(0, project_data.get('color', '#3B82F6'))
        
        # Order
        tk.Label(dialog, text="[ORDER]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['order'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['order'].pack(fill=tk.X, padx=5, pady=2)
        entries['order'].insert(0, str(project_data.get('order', 1)))
        
        def save_project_data():
            self.ideas_data[self.current_idea_id]['project_data'] = {
                'image': entries['image'].get().strip(),
                'tags': [t.strip() for t in entries['tags'].get().split(',') if t.strip()],
                'tech': [t.strip() for t in entries['tech'].get().split(',') if t.strip()],
                'color': entries['color'].get().strip(),
                'order': int(entries['order'].get()) if entries['order'].get().isdigit() else 1
            }
            self.save_ideas_to_file()
            self.show_notification("Project data saved", "success")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="[S]SAVE", command=save_project_data, bg=self.colors['success'], fg='#000000', font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="[ESC]CANCEL", command=dialog.destroy, bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
    
    def edit_certification_data(self):
        """Editar datos específicos para certification"""
        if self.current_idea_id is None or self.current_idea_id >= len(self.ideas_data):
            self.show_notification("Select an idea first", "warning")
            return
        
        cert_data = self.ideas_data[self.current_idea_id].get('certification_data', {})
        
        dialog = tk.Toplevel(self.root)
        dialog.title("[EDIT CERT DATA]")
        dialog.geometry("400x350")
        dialog.configure(bg=self.colors['bg'])
        
        entries = {}
        
        # Icon
        tk.Label(dialog, text="[ICON]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['icon'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['icon'].pack(fill=tk.X, padx=5, pady=2)
        entries['icon'].insert(0, cert_data.get('icon', 'big'))
        
        # Issuer
        tk.Label(dialog, text="[ISSUER]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['issuer'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['issuer'].pack(fill=tk.X, padx=5, pady=2)
        entries['issuer'].insert(0, cert_data.get('issuer', 'Unknown'))
        
        # Date
        tk.Label(dialog, text="[DATE]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['date'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['date'].pack(fill=tk.X, padx=5, pady=2)
        entries['date'].insert(0, cert_data.get('date', datetime.now().strftime('%Y')))
        
        # Credential ID
        tk.Label(dialog, text="[CREDENTIAL ID]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['credentialId'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['credentialId'].pack(fill=tk.X, padx=5, pady=2)
        entries['credentialId'].insert(0, cert_data.get('credentialId', ''))
        
        # Badge
        tk.Label(dialog, text="[BADGE]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['badge'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['badge'].pack(fill=tk.X, padx=5, pady=2)
        entries['badge'].insert(0, cert_data.get('badge', 'None'))
        
        def save_cert_data():
            self.ideas_data[self.current_idea_id]['certification_data'] = {
                'icon': entries['icon'].get().strip(),
                'issuer': entries['issuer'].get().strip(),
                'date': entries['date'].get().strip(),
                'credentialId': entries['credentialId'].get().strip(),
                'badge': entries['badge'].get().strip()
            }
            self.save_ideas_to_file()
            self.show_notification("Certification data saved", "success")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="[S]SAVE", command=save_cert_data, bg=self.colors['success'], fg='#000000', font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="[ESC]CANCEL", command=dialog.destroy, bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
    
    def edit_secondary_project_data(self):
        """Editar datos específicos para secondary project"""
        if self.current_idea_id is None or self.current_idea_id >= len(self.ideas_data):
            self.show_notification("Select an idea first", "warning")
            return
        
        sec_data = self.ideas_data[self.current_idea_id].get('secondary_project_data', {})
        
        dialog = tk.Toplevel(self.root)
        dialog.title("[EDIT SEC PROJ DATA]")
        dialog.geometry("400x400")
        dialog.configure(bg=self.colors['bg'])
        
        entries = {}
        
        # Category
        tk.Label(dialog, text="[CATEGORY]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['category'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['category'].pack(fill=tk.X, padx=5, pady=2)
        entries['category'].insert(0, sec_data.get('category', 'General'))
        
        # Description
        tk.Label(dialog, text="[DESCRIPTION]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['description'] = tk.Text(dialog, height=3, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['description'].pack(fill=tk.X, padx=5, pady=2)
        entries['description'].insert(1.0, sec_data.get('description', ''))
        
        # Details
        tk.Label(dialog, text="[DETAILS]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['details'] = tk.Text(dialog, height=3, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['details'].pack(fill=tk.X, padx=5, pady=2)
        entries['details'].insert(1.0, sec_data.get('details', ''))
        
        # Tech
        tk.Label(dialog, text="[TECH STACK]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['tech'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['tech'].pack(fill=tk.X, padx=5, pady=2)
        entries['tech'].insert(0, ', '.join(sec_data.get('tech', [])))
        
        # Link
        tk.Label(dialog, text="[LINK URL]:", bg=self.colors['bg'], fg=self.colors['text_primary'], font=self.terminal_font_bold).pack(anchor=tk.W, padx=5, pady=(5, 2))
        entries['link'] = tk.Entry(dialog, bg=self.colors['bg_card'], fg=self.colors['text_primary'], insertbackground=self.colors['accent'], font=self.terminal_font, relief=tk.FLAT, bd=1)
        entries['link'].pack(fill=tk.X, padx=5, pady=2)
        entries['link'].insert(0, sec_data.get('link', ''))
        
        def save_sec_data():
            self.ideas_data[self.current_idea_id]['secondary_project_data'] = {
                'category': entries['category'].get().strip(),
                'description': entries['description'].get(1.0, tk.END).strip(),
                'details': entries['details'].get(1.0, tk.END).strip(),
                'tech': [t.strip() for t in entries['tech'].get().split(',') if t.strip()],
                'link': entries['link'].get().strip()
            }
            self.save_ideas_to_file()
            self.show_notification("Secondary project data saved", "success")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="[S]SAVE", command=save_sec_data, bg=self.colors['success'], fg='#000000', font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="[ESC]CANCEL", command=dialog.destroy, bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=self.terminal_font_bold, relief=tk.FLAT, bd=1, padx=10, pady=4).pack(side=tk.LEFT, padx=2)
    
    def convert_to_post(self):
        """Convertir la idea en un post real"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        if not content:
            self.show_notification("Content is required", "warning")
            return
        
        # Cargar posts existentes
        try:
            posts_path = self.base_path / 'posts.json'
            if posts_path.exists():
                with open(posts_path, 'r', encoding='utf-8') as f:
                    posts_data = json.load(f)
            else:
                posts_data = []
        except:
            posts_data = []
        
        # Obtener datos específicos de post si existen
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            post_data = self.ideas_data[self.current_idea_id].get('post_data', {})
        else:
            post_data = {}
        
        # Extraer primera línea como título
        lines = content.split('\n')
        title = lines[0].strip() if lines else 'Untitled'
        # El resto del contenido es el body
        body = '\n'.join(lines[1:]) if len(lines) > 1 else content
        
        # Crear nuevo post desde la idea, usando datos específicos si existen
        new_post = {
            'id': str(len(posts_data) + 1),
            'slug': post_data.get('slug', title.lower().replace(' ', '-').replace('/', '-')),
            'title': title,
            'category': post_data.get('category', 'Development'),
            'description': post_data.get('description', body[:200] + '...' if len(body) > 200 else body),
            'content': body,
            'createdAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'keywords': post_data.get('keywords', []),
            'readingTime': post_data.get('readingTime', 5),
            'wordCount': 1000,
            'featured': post_data.get('featured', False),
            'published': post_data.get('published', False),
            'series': None,
            'seriesOrder': None,
            'seriesPartTitle': None
        }
        
        posts_data.append(new_post)
        
        # Guardar posts
        try:
            with open(posts_path, 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, indent=2, ensure_ascii=False)
            self.save_file()
            self.show_notification("Post created successfully", "success")
            
            # Auto-eliminar la idea después de convertirla (estilo terminal)
            if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
                del self.ideas_data[self.current_idea_id]
                self.save_ideas_to_file()
                self.update_ideas_listbox()
                self.new_idea()
                self.show_notification("Idea deleted after conversion", "info")
        except Exception as e:
            self.show_notification(f"Error creating post: {str(e)}", "error")
    
    def convert_to_project(self):
        """Convertir la idea en un proyecto real"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        if not content:
            self.show_notification("Content is required", "warning")
            return
        
        # Cargar proyectos existentes
        try:
            projects_path = self.base_path / 'projects.json'
            if projects_path.exists():
                with open(projects_path, 'r', encoding='utf-8') as f:
                    projects_data = json.load(f)
            else:
                projects_data = []
        except:
            projects_data = []
        
        # Obtener datos específicos de proyecto si existen
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            project_data = self.ideas_data[self.current_idea_id].get('project_data', {})
        else:
            project_data = {}
        
        # Extraer primera línea como título
        lines = content.split('\n')
        title = lines[0].strip() if lines else 'Untitled'
        # El resto del contenido es la descripción
        description = '\n'.join(lines[1:]) if len(lines) > 1 else content
        
        # Crear nuevo proyecto desde la idea, usando datos específicos si existen
        new_project = {
            'id': str(len(projects_data) + 1),
            'title': title,
            'description': project_data.get('description', description),
            'image': project_data.get('image', '/images/default.png'),
            'tags': project_data.get('tags', []),
            'tech': project_data.get('tech', []),
            'color': project_data.get('color', '#3B82F6'),
            'order': project_data.get('order', len(projects_data) + 1),
            'relatedPostIds': []
        }
        
        projects_data.append(new_project)
        
        # Guardar proyectos
        try:
            with open(projects_path, 'w', encoding='utf-8') as f:
                json.dump(projects_data, f, indent=2, ensure_ascii=False)
            self.save_file()
            self.show_notification("Project created successfully", "success")
            
            # Auto-eliminar la idea después de convertirla (estilo terminal)
            if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
                del self.ideas_data[self.current_idea_id]
                self.save_ideas_to_file()
                self.update_ideas_listbox()
                self.new_idea()
                self.show_notification("Idea deleted after conversion", "info")
        except Exception as e:
            self.show_notification(f"Error creating project: {str(e)}", "error")
    
    def convert_to_certification(self):
        """Convertir la idea en una certificación real"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        if not content:
            self.show_notification("Content is required", "warning")
            return
        
        # Cargar certificaciones existentes
        try:
            certifications_path = self.base_path / 'certifications.json'
            if certifications_path.exists():
                with open(certifications_path, 'r', encoding='utf-8') as f:
                    certifications_data = json.load(f)
            else:
                certifications_data = []
        except:
            certifications_data = []
        
        # Obtener datos específicos de certificación si existen
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            cert_data = self.ideas_data[self.current_idea_id].get('certification_data', {})
        else:
            cert_data = {}
        
        # Extraer primera línea como nombre
        lines = content.split('\n')
        name = lines[0].strip() if lines else 'Untitled'
        
        # Crear nueva certificación desde la idea, usando datos específicos si existen
        new_certification = {
            'id': str(len(certifications_data) + 1),
            'name': name,
            'icon': cert_data.get('icon', 'big'),
            'order': len(certifications_data) + 1,
            'issuer': cert_data.get('issuer', 'Unknown'),
            'date': cert_data.get('date', datetime.now().strftime('%Y')),
            'credentialId': cert_data.get('credentialId', ''),
            'badge': cert_data.get('badge', 'None'),
            'relatedPostId': None
        }
        
        certifications_data.append(new_certification)
        
        # Guardar certificaciones
        try:
            with open(certifications_path, 'w', encoding='utf-8') as f:
                json.dump(certifications_data, f, indent=2, ensure_ascii=False)
            self.save_file()
            self.show_notification("Certification created successfully", "success")
            
            # Auto-eliminar la idea después de convertirla (estilo terminal)
            if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
                del self.ideas_data[self.current_idea_id]
                self.save_ideas_to_file()
                self.update_ideas_listbox()
                self.new_idea()
                self.show_notification("Idea deleted after conversion", "info")
        except Exception as e:
            self.show_notification(f"Error creating certification: {str(e)}", "error")
    
    def convert_to_secondary_project(self):
        """Convertir la idea en un proyecto secundario real"""
        content = self.idea_content_text.get(1.0, tk.END).strip()
        if not content:
            self.show_notification("Content is required", "warning")
            return
        
        # Cargar proyectos secundarios existentes
        try:
            secondary_projects_path = self.base_path / 'secondary-projects.json'
            if secondary_projects_path.exists():
                with open(secondary_projects_path, 'r', encoding='utf-8') as f:
                    secondary_projects_data = json.load(f)
            else:
                secondary_projects_data = {}
        except:
            secondary_projects_data = {}
        
        # Obtener datos específicos de proyecto secundario si existen
        if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
            sec_data = self.ideas_data[self.current_idea_id].get('secondary_project_data', {})
        else:
            sec_data = {}
        
        # Extraer primera línea como nombre
        lines = content.split('\n')
        name = lines[0].strip() if lines else 'Untitled'
        # El resto del contenido es la descripción
        description = '\n'.join(lines[1:]) if len(lines) > 1 else content
        
        category = sec_data.get('category', 'General')
        if category not in secondary_projects_data:
            secondary_projects_data[category] = []
        
        # Calcular el siguiente ID
        all_projects = []
        for cat_projects in secondary_projects_data.values():
            all_projects.extend(cat_projects)
        next_id = len(all_projects) + 1
        
        # Crear nuevo proyecto secundario desde la idea, usando datos específicos si existen
        new_secondary_project = {
            'id': str(next_id),
            'name': name,
            'description': sec_data.get('description', description),
            'details': sec_data.get('details', ''),
            'tech': sec_data.get('tech', []),
            'link': sec_data.get('link', ''),
            'relatedPostIds': [],
            'category': category
        }
        
        secondary_projects_data[category].append(new_secondary_project)
        
        # Guardar proyectos secundarios
        try:
            with open(secondary_projects_path, 'w', encoding='utf-8') as f:
                json.dump(secondary_projects_data, f, indent=2, ensure_ascii=False)
            self.save_file()
            self.show_notification("Secondary project created successfully", "success")
            
            # Auto-eliminar la idea después de convertirla (estilo terminal)
            if self.current_idea_id is not None and self.current_idea_id < len(self.ideas_data):
                del self.ideas_data[self.current_idea_id]
                self.save_ideas_to_file()
                self.update_ideas_listbox()
                self.new_idea()
                self.show_notification("Idea deleted after conversion", "info")
        except Exception as e:
            self.show_notification(f"Error creating secondary project: {str(e)}", "error")


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()
