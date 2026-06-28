#!/usr/bin/env python3
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
import re
from datetime import datetime
from PIL import Image, ImageTk

class JSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("BLANCH.CC JSON EDITOR")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Configurar estilo cyberpunk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#0a0a0a')
        self.style.configure('TLabel', background='#0a0a0a', foreground='#ff0040', font=('Orbitron', 10))
        self.style.configure('TButton', background='#ff0040', foreground='#000000', font=('Orbitron', 10, 'bold'))
        self.style.configure('TNotebook', background='#0a0a0a')
        self.style.configure('TNotebook.Tab', background='#1a0a0a', foreground='#ff0040', padding=[15, 8], font=('Orbitron', 9, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#ff0040')], foreground=[('selected', '#000000')])
        
        self.root.configure(bg='#0a0a0a')
        
        # Ruta base del proyecto
        self.base_path = Path(__file__).parent / 'src' / 'data'
        self.public_path = Path(__file__).parent / 'public'
        self.cert_images = {}
        
        # Archivos JSON disponibles
        self.json_files = {
            'Certificaciones': 'certifications.json',
            'Posts': 'posts.json',
            'Proyectos': 'projects.json',
            'Proyectos Secundarios': 'secondary-projects.json',
            'Servicios': 'services.json'
        }
        
        self.current_data = None
        self.current_file = None
        self.unsaved_changes = False
        self.showing_dashboard = True
        
        self.create_ui()
        self.show_dashboard()
    
    def create_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header con estilo futurista
        header_frame = tk.Frame(main_frame, bg='#0a0a0a')
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Línea decorativa con efecto neón
        tk.Frame(header_frame, bg='#ff0040', height=3).pack(fill=tk.X, pady=(0, 15))
        
        self.title_label = tk.Label(header_frame, text="⚡ CYBERPUNK JSON EDITOR // NIL BLANCH ⚡", 
                              font=('Orbitron', 20, 'bold'), bg='#0a0a0a', fg='#ff0040')
        self.title_label.pack(side=tk.LEFT)
        
        # Botón de cierre
        close_btn = tk.Button(header_frame, text="✕ CLOSE", 
                            command=self.root.destroy,
                            font=('Orbitron', 10, 'bold'), 
                            bg='#ff0040', fg='#000000', 
                            activebackground='#cc0033', activeforeground='#000000',
                            relief=tk.RAISED, cursor='hand2', bd=2, padx=15, pady=8)
        close_btn.pack(side=tk.RIGHT)
        
        # Selector de archivo con estilo - botones grandes
        selector_frame = tk.Frame(main_frame, bg='#0a0a0a')
        selector_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid de botones para cada archivo
        self.file_buttons = {}
        button_grid = tk.Frame(selector_frame, bg='#0a0a0a')
        button_grid.pack(fill=tk.X)
        
        btn_style_large = {'font': ('Orbitron', 12, 'bold'), 'bg': '#1a0a0a', 'fg': '#ff0040', 
                          'activebackground': '#ff0040', 'activeforeground': '#000000',
                          'relief': tk.RAISED, 'cursor': 'hand2', 'bd': 3, 'padx': 25, 'pady': 12,
                          'highlightbackground': '#ff0040', 'highlightthickness': 2}
        
        for idx, (name, file) in enumerate(self.json_files.items()):
            btn = tk.Button(button_grid, text=name, 
                          command=lambda f=file: self.load_specific_file(f),
                          **btn_style_large)
            btn.grid(row=0, column=idx, padx=8, pady=5, sticky='ew')
            button_grid.grid_columnconfigure(idx, weight=1)
            self.file_buttons[file] = btn
        
        # Botones de acción
        action_btn_frame = tk.Frame(selector_frame, bg='#0a0a0a')
        action_btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        btn_style_action = {'font': ('Orbitron', 11, 'bold'), 'bg': '#ff0040', 'fg': '#000000', 
                           'activebackground': '#cc0033', 'activeforeground': '#000000',
                           'relief': tk.RAISED, 'cursor': 'hand2', 'bd': 2, 'padx': 25, 'pady': 10}
        
        save_btn = tk.Button(action_btn_frame, text="💾 SAVE", command=self.save_file, **btn_style_action)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = tk.Button(action_btn_frame, text="🔄 REFRESH", command=self.refresh_file, **btn_style_action)
        refresh_btn.pack(side=tk.LEFT)
        
        # Notebook para diferentes vistas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Vista dashboard
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text='DASHBOARD')
        
        # Vista visual por tipo de JSON
        self.visual_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visual_frame, text='VISUAL VIEW')
        
        # Editor de texto para JSON raw
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='RAW JSON')
        
        # Editor de elementos
        self.editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text='EDITOR')
        
        self.create_visual_view()
        self.create_text_editor()
        self.create_dashboard()
        self.create_element_editor()
        
        # Configurar atajos de teclado
        self.setup_keyboard_shortcuts()
        
        # Iniciar animaciones
        self.animate_title()
        self.animate_neon_border()
        self.animate_status_bar()
        
        # Línea decorativa
        tk.Frame(main_frame, bg='#ff0040', height=3).pack(fill=tk.X, pady=(20, 15))
        
        # Botones de acción
        action_frame = tk.Frame(main_frame, bg='#0a0a0a')
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_style = {'font': ('Orbitron', 10, 'bold'), 'bg': '#ff0040', 'fg': '#000000', 
                     'activebackground': '#cc0033', 'activeforeground': '#000000',
                     'relief': tk.RAISED, 'cursor': 'hand2', 'bd': 2}
        
        tk.Button(action_frame, text="+ ADD", command=self.add_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(action_frame, text="✏ EDIT", command=self.edit_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(action_frame, text="🗑 DELETE", command=self.delete_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar con estilo
        self.status_var = tk.StringVar()
        self.status_var.set("READY // SELECT A FILE TO BEGIN")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                            font=('Orbitron', 9), bg='#0a0a0a', fg='#ff0040', 
                            relief=tk.FLAT, pady=10)
        status_bar.pack(fill=tk.X)
        
        # Indicador de cambios sin guardar
        self.unsaved_label = tk.Label(main_frame, text="", 
                                     font=('Orbitron', 10, 'bold'), 
                                     bg='#0a0a0a', fg='#ff0040')
        self.unsaved_label.pack(fill=tk.X, pady=(5, 0))
    
    def create_visual_view(self):
        # Scrollbars
        visual_scroll_y = ttk.Scrollbar(self.visual_frame)
        visual_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        visual_scroll_x = ttk.Scrollbar(self.visual_frame, orient=tk.HORIZONTAL)
        visual_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas para vista visual
        self.visual_canvas = tk.Canvas(self.visual_frame, bg='#0a0a0a', yscrollcommand=visual_scroll_y.set, xscrollcommand=visual_scroll_x.set, highlightthickness=0)
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
        
        # Bind events para scroll del ratón (Linux usa Button-4/5, Windows/Mac usan MouseWheel)
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
        
        # Text widget
        self.text_editor = tk.Text(self.text_frame, yscrollcommand=text_scroll.set, bg='#0a0a0a', fg='#ff0040', font=('Orbitron', 11), insertbackground='#ff0040')
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Detectar cambios en el editor de texto
        self.text_editor.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        self.text_editor.bind('<ButtonRelease-1>', lambda e: self.mark_unsaved())
        
        text_scroll.config(command=self.text_editor.yview)
    
    def create_element_editor(self):
        # Scrollable frame para el editor
        self.editor_scroll_y = ttk.Scrollbar(self.editor_frame)
        self.editor_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.editor_canvas = tk.Canvas(self.editor_frame, bg='#0a0a0a', yscrollcommand=self.editor_scroll_y.set, highlightthickness=0)
        self.editor_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.editor_scroll_y.config(command=self.editor_canvas.yview)
        
        # Bind para scroll con ratón
        try:
            self.editor_canvas.bind('<MouseWheel>', lambda e: self.editor_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        except:
            pass
        self.editor_canvas.bind('<Button-4>', lambda e: self.editor_canvas.yview_scroll(-1, "units"))
        self.editor_canvas.bind('<Button-5>', lambda e: self.editor_canvas.yview_scroll(1, "units"))
        
        self.editor_scrollable_frame = tk.Frame(self.editor_canvas, bg='#0a0a0a')
        self.editor_canvas.create_window((0, 0), window=self.editor_scrollable_frame, anchor="nw")
        
        self.editor_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))
        )
        
        self.editor_entries = {}
        self.editor_mode = None  # 'add' or 'edit'
        self.editor_element = None
        
        # Botones de acción del editor
        self.editor_button_frame = tk.Frame(self.editor_scrollable_frame, bg='#0a0a0a')
        self.editor_button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_style = {'font': ('Orbitron', 10, 'bold'), 'bg': '#ff0040', 'fg': '#000000', 
                     'activebackground': '#cc0033', 'activeforeground': '#000000',
                     'relief': tk.RAISED, 'cursor': 'hand2', 'bd': 2, 'padx': 20, 'pady': 8}
        
        tk.Button(self.editor_button_frame, text="SAVE", command=self.save_editor, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(self.editor_button_frame, text="CANCEL", command=self.cancel_editor, **btn_style).pack(side=tk.LEFT)
    
    def create_dashboard(self):
        # Frame principal del dashboard
        dash_main = tk.Frame(self.dashboard_frame, bg='#0a0a0a')
        dash_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título del dashboard
        title_frame = tk.Frame(dash_main, bg='#0a0a0a')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(title_frame, text="⚡ DASHBOARD // ESTADÍSTICAS Y ACCIONES RÁPIDAS ⚡", 
                font=('Orbitron', 16, 'bold'), bg='#0a0a0a', fg='#ff0040').pack(anchor=tk.W)
        
        # Frame para estadísticas
        stats_frame = tk.Frame(dash_main, bg='#0a0a0a')
        stats_frame.pack(fill=tk.X, pady=(0, 30))
        
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
        
        # Crear tarjetas de estadísticas
        stats_grid = tk.Frame(stats_frame, bg='#0a0a0a')
        stats_grid.pack(fill=tk.X)
        
        for idx, (name, count) in enumerate(self.dashboard_stats.items()):
            card = tk.Frame(stats_grid, bg='#1a0a0a', bd=2, relief=tk.FLAT, highlightbackground='#ff0040', highlightthickness=2)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky='nsew')
            stats_grid.grid_columnconfigure(idx, weight=1)
            
            tk.Label(card, text=name.upper(), font=('Orbitron', 10, 'bold'), 
                    bg='#1a0a0a', fg='#ff0040').pack(pady=(15, 5))
            tk.Label(card, text=str(count), font=('Orbitron', 24, 'bold'), 
                    bg='#1a0a0a', fg='#ff0040').pack(pady=(0, 15))
            
            # Hacer la tarjeta clickeable
            card.bind('<Button-1>', lambda e, f=self.json_files[name]: self.load_specific_file(f))
        
        # Frame para acciones rápidas
        actions_frame = tk.Frame(dash_main, bg='#0a0a0a')
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(actions_frame, text="⚡ ACCIONES RÁPIDAS ⚡", 
                font=('Orbitron', 14, 'bold'), bg='#0a0a0a', fg='#ff0040').pack(anchor=tk.W, pady=(0, 20))
        
        # Botones grandes para cargar archivos
        btn_grid = tk.Frame(actions_frame, bg='#0a0a0a')
        btn_grid.pack(fill=tk.BOTH, expand=True)
        
        btn_style_large = {'font': ('Orbitron', 12, 'bold'), 'bg': '#ff0040', 'fg': '#000000', 
                          'activebackground': '#cc0033', 'activeforeground': '#000000',
                          'relief': tk.RAISED, 'cursor': 'hand2', 'bd': 2, 'padx': 30, 'pady': 15}
        
        for idx, (name, file) in enumerate(self.json_files.items()):
            btn = tk.Button(btn_grid, text=f"📂 {name.upper()}", 
                          command=lambda f=file: self.load_specific_file(f),
                          **btn_style_large)
            btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=10, sticky='nsew')
        
        btn_grid.grid_columnconfigure(0, weight=1)
        btn_grid.grid_columnconfigure(1, weight=1)
        btn_grid.grid_rowconfigure(0, weight=1)
        btn_grid.grid_rowconfigure(1, weight=1)
        btn_grid.grid_rowconfigure(2, weight=1)
    
    def show_dashboard(self):
        self.notebook.select(0)
    
    def load_specific_file(self, json_file):
        # Verificar si hay cambios sin guardar
        if self.unsaved_changes:
            if not messagebox.askyesno("Cambios sin guardar", "Hay cambios sin guardar. ¿Deseas guardar antes de cargar otro archivo?"):
                self.unsaved_changes = False
            else:
                self.save_file()
        
        file_path = self.base_path / json_file
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_data = json.load(f)
                self.current_file = json_file
            
            self.update_visual_view()
            self.update_text_editor()
            self.status_var.set(f"Archivo cargado: {json_file}")
            self.unsaved_changes = False
            self.unsaved_label.config(text="")
            
            # Actualizar botones para mostrar el archivo activo
            for file, btn in self.file_buttons.items():
                if file == json_file:
                    btn.config(bg='#00ff00', fg='#000000', activebackground='#00cc00')
                else:
                    btn.config(bg='#1a1a1a', fg='#00ff00', activebackground='#00ff00')
            
            # Cambiar automáticamente a la vista visual al cargar un archivo
            self.notebook.select(1)
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {file_path}")
            self.status_var.set("Error: Archivo no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error al decodificar JSON: {file_path}")
            self.status_var.set("Error: JSON inválido")
    
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
    
    def create_posts_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 320
        card_height = 200
        gap = 15
        
        for idx, post in enumerate(self.current_data):
            if idx > 0 and idx % 5 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background con estilo cyberpunk
            card = self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a0a0a', outline='#ff0040', width=2,
                tags=('card', f'post_{idx}')
            )
            
            # Title con wrapping
            title = post.get('title', 'Sin título')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=title,
                font=('Orbitron', 11, 'bold'),
                fill='#ff0040', anchor='nw',
                width=card_width - 30,
                tags=('card', f'post_{idx}')
            )
            
            # Category badge
            category = post.get('category', '') or ''
            self.visual_canvas.create_rectangle(
                x_pos + 15, y_pos + 50, x_pos + 15 + len(category) * 8 + 20, y_pos + 70,
                fill='#ff0040', outline='#ff0040',
                tags=('card', f'post_{idx}')
            )
            self.visual_canvas.create_text(
                x_pos + 25, y_pos + 52,
                text=category.upper(),
                font=('Orbitron', 8, 'bold'),
                fill='#000000', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Description con wrapping
            desc = post.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 80,
                text=desc,
                font=('Orbitron', 9),
                fill='#cc0033', anchor='nw',
                width=card_width - 30,
                tags=('card', f'post_{idx}')
            )
            
            # Date
            date = post.get('createdAt', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + card_height - 25,
                text=date,
                font=('Orbitron', 8),
                fill='#ff0040', anchor='nw',
                width=card_width - 30,
                tags=('card', f'post_{idx}')
            )
            
            # Featured indicator
            if post.get('featured', False):
                self.visual_canvas.create_text(
                    x_pos + card_width - 25, y_pos + 15,
                    text="⚡",
                    font=('Orbitron', 14),
                    fill='#ff0040', anchor='ne',
                    tags=('card', f'post_{idx}')
                )
            
            self.visual_elements.append({'type': 'post', 'index': idx, 'data': post, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        # Update scroll region
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_projects_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 280
        card_height = 180
        gap = 12
        
        for idx, project in enumerate(self.current_data):
            if idx > 0 and idx % 6 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background con color personalizado
            color = project.get('color', '#ff0040')
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a0a0a', outline=color, width=3,
                tags=('card', f'project_{idx}')
            )
            
            # Title con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=project.get('title', 'Sin título'),
                font=('Orbitron', 11, 'bold'),
                fill='#ff0040', anchor='nw',
                width=card_width - 30,
                tags=('card', f'project_{idx}')
            )
            
            # Description con wrapping
            desc = project.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 45,
                text=desc,
                font=('Orbitron', 9),
                fill='#cc0033', anchor='nw',
                width=card_width - 30,
                tags=('card', f'project_{idx}')
            )
            
            # Tags con wrapping
            tags = project.get('tags', [])
            if tags:
                tags_text = ', '.join(tags[:4])
                self.visual_canvas.create_text(
                    x_pos + 15, y_pos + card_height - 35,
                    text=tags_text,
                    font=('Consolas', 8),
                    fill=color, anchor='nw',
                    width=card_width - 30,
                    tags=('card', f'project_{idx}')
                )
            
            self.visual_elements.append({'type': 'project', 'index': idx, 'data': project, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_certifications_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 260
        card_height = 140
        gap = 12
        
        for idx, cert in enumerate(self.current_data):
            if idx > 0 and idx % 6 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a0a0a', outline='#ff0040', width=2,
                tags=('card', f'cert_{idx}')
            )
            
            # Icon image - usar badge si existe, sino usar icon
            badge_url = cert.get('badge', '')
            icon_name = cert.get('icon', '')
            
            if badge_url:
                # Si hay badge, mostrar texto indicando que hay badge
                self.visual_canvas.create_text(
                    x_pos + card_width - 40, y_pos + 20,
                    text="🏆",
                    font=('Orbitron', 24),
                    fill='#ff0040',
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
    
    def _show_cert_fallback(self, x_pos, y_pos, card_width, cert, idx):
        """Mostrar fallback con primera letra del issuer"""
        issuer = cert.get('issuer', '')
        first_letter = issuer[0].upper() if issuer else '?'
        self.visual_canvas.create_oval(
            x_pos + card_width - 55, y_pos + 10,
            x_pos + card_width - 25, y_pos + 40,
            fill='#1a0a0a', outline='#ff0040', width=2,
            tags=('card', f'cert_{idx}')
        )
        self.visual_canvas.create_text(
            x_pos + card_width - 40, y_pos + 25,
            text=first_letter,
            font=('Orbitron', 16, 'bold'),
            fill='#ff0040',
            tags=('card', f'cert_{idx}')
        )
            
            # Name con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=cert.get('name', 'Sin nombre'),
                font=('Orbitron', 10, 'bold'),
                fill='#ff0040', anchor='nw',
                width=card_width - 80,
                tags=('card', f'cert_{idx}')
            )
            
            # Issuer
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 50,
                text=f"Issuer: {cert.get('issuer', '')}",
                font=('Orbitron', 9),
                fill='#cc0033', anchor='nw',
                width=card_width - 80,
                tags=('card', f'cert_{idx}')
            )
            
            # Date
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + card_height - 35,
                text=f"Date: {cert.get('date', '')}",
                font=('Orbitron', 8),
                fill='#ff0040', anchor='nw',
                width=card_width - 30,
                tags=('card', f'cert_{idx}')
            )
            
            # Credential ID
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + card_height - 20,
                text=f"ID: {cert.get('credentialId', '')}",
                font=('Orbitron', 7),
                fill='#cc0033', anchor='nw',
                width=card_width - 30,
                tags=('card', f'cert_{idx}')
            )
            
            self.visual_elements.append({'type': 'cert', 'index': idx, 'data': cert, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_services_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 300
        card_height = 130
        gap = 12
        
        for idx, service in enumerate(self.current_data):
            if idx > 0 and idx % 5 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a0a0a', outline='#ff0040', width=2,
                tags=('card', f'service_{idx}')
            )
            
            # Title con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=service.get('title', 'Sin título'),
                font=('Orbitron', 11, 'bold'),
                fill='#ff0040', anchor='nw',
                width=card_width - 30,
                tags=('card', f'service_{idx}')
            )
            
            # Description con wrapping
            desc = service.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 40,
                text=desc,
                font=('Orbitron', 9),
                fill='#cc0033', anchor='nw',
                width=card_width - 30,
                tags=('card', f'service_{idx}')
            )
            
            # Order indicator
            order = service.get('order', 0)
            self.visual_canvas.create_text(
                x_pos + card_width - 15, y_pos + card_height - 15,
                text=f"#{order}",
                font=('Orbitron', 10, 'bold'),
                fill='#ff0040', anchor='se',
                tags=('card', f'service_{idx}')
            )
            
            self.visual_elements.append({'type': 'service', 'index': idx, 'data': service, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_secondary_projects_view(self):
        y_pos = 20
        x_pos = 20
        
        for category, projects in self.current_data.items():
            if isinstance(projects, list):
                # Category header con estilo
                self.visual_canvas.create_rectangle(
                    x_pos, y_pos, x_pos + 200, y_pos + 30,
                    fill='#ff0040', outline='#ff0040',
                    tags=('header', f'cat_{category}')
                )
                self.visual_canvas.create_text(
                    x_pos + 10, y_pos + 5,
                    text=category.upper(),
                    font=('Orbitron', 11, 'bold'),
                    fill='#000000', anchor='nw',
                    tags=('header', f'cat_{category}')
                )
                y_pos += 40
                
                # Projects in category
                card_width = 280
                card_height = 120
                gap = 12
                
                for idx, project in enumerate(projects):
                    if idx > 0 and idx % 5 == 0:
                        x_pos = 20
                        y_pos += card_height + gap
                    
                    # Card background
                    self.visual_canvas.create_rectangle(
                        x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                        fill='#1a0a0a', outline='#ff0040', width=2,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Name con wrapping
                    self.visual_canvas.create_text(
                        x_pos + 15, y_pos + 15,
                        text=project.get('name', 'Sin nombre'),
                        font=('Orbitron', 10, 'bold'),
                        fill='#ff0040', anchor='nw',
                        width=card_width - 30,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Description con wrapping
                    desc = project.get('description', '')
                    self.visual_canvas.create_text(
                        x_pos + 15, y_pos + 40,
                        text=desc,
                        font=('Orbitron', 9),
                        fill='#cc0033', anchor='nw',
                        width=card_width - 30,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Tech con wrapping
                    tech = project.get('tech', [])
                    if tech:
                        tech_text = ', '.join(tech[:3])
                        self.visual_canvas.create_text(
                            x_pos + 15, y_pos + card_height - 30,
                            text=tech_text,
                            font=('Orbitron', 8),
                            fill='#ff0040', anchor='nw',
                            width=card_width - 30,
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
        if self.selected_element:
            self.edit_element()
    
    def highlight_selected(self, element):
        # Remover highlight anterior
        self.visual_canvas.delete('highlight')
        
        # Añadir highlight al elemento seleccionado
        x, y = element['x'], element['y']
        width, height = element['width'], element['height']
        
        self.visual_canvas.create_rectangle(
            x - 2, y - 2, x + width + 2, y + height + 2,
            outline='#ffffff', width=3,
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
                outline='#ffffff', width=3,
                tags='highlight'
            )
    
    def on_double_click(self, event):
        self.edit_element()
    
    def add_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        self.editor_mode = 'add'
        self.editor_element = None
        self.populate_editor()
        self.notebook.select(3)  # Ir a la pestaña EDITOR
    
    def edit_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        if not self.selected_element:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para editar (doble click en la tarjeta)")
            return
        
        self.editor_mode = 'edit'
        self.editor_element = self.selected_element
        self.populate_editor(self.selected_element['data'])
        self.notebook.select(3)  # Ir a la pestaña EDITOR
    
    def delete_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        if not self.selected_element:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para eliminar (click en la tarjeta)")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este elemento?"):
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
                            self.status_var.set("Elemento eliminado")
                            self.selected_element = None
                            self.visual_canvas.delete('highlight')
                        except (ValueError, IndexError):
                            messagebox.showerror("Error", "No se pudo eliminar el elemento")
                return
            
            # Manejar estructura normal (list)
            index = element['index']
            
            if isinstance(self.current_data, list):
                try:
                    del self.current_data[index]
                    self.update_visual_view()
                    self.update_text_editor()
                    self.mark_unsaved()
                    self.status_var.set("Elemento eliminado")
                    self.selected_element = None
                    self.visual_canvas.delete('highlight')
                except (ValueError, IndexError):
                    messagebox.showerror("Error", "No se pudo eliminar el elemento")
    
    def save_file(self):
        if not self.current_data or not self.current_file:
            messagebox.showwarning("Advertencia", "No hay datos para guardar")
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
            messagebox.showinfo("Éxito", f"Archivo guardado: {self.current_file}")
            self.status_var.set(f"Archivo guardado: {self.current_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar archivo: {str(e)}")
            self.status_var.set("Error al guardar archivo")
    
    def mark_unsaved(self):
        self.unsaved_changes = True
        self.unsaved_label.config(text="⚠️ HAY CAMBIOS SIN GUARDAR")
    
    def animate_title(self):
        """Animación del título con efecto de parpadeo"""
        colors = ['#ff0040', '#cc0033', '#ff0040', '#ff6666']
        self.title_color_index = 0
        
        def pulse():
            if hasattr(self, 'title_label'):
                color = colors[self.title_color_index]
                self.title_label.config(fg=color)
                self.title_color_index = (self.title_color_index + 1) % len(colors)
                self.root.after(500, pulse)
        
        self.root.after(500, pulse)
    
    def animate_neon_border(self):
        """Animación de borde neón en las tarjetas seleccionadas"""
        self.neon_colors = ['#ff0040', '#ff6666', '#ff0040', '#cc0033']
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
                self.root.after(300, pulse_neon)
        
        self.root.after(300, pulse_neon)
    
    def animate_status_bar(self):
        """Animación de la barra de estado con mensajes cíclicos"""
        messages = [
            "READY // SYSTEM ONLINE",
            "⚡ BLANCH.CC JSON EDITOR ⚡",
            "PRESS ESC TO EXIT FULLSCREEN",
            "DOUBLE-CLICK TO EDIT ELEMENTS"
        ]
        self.message_index = 0
        
        def cycle_messages():
            if hasattr(self, 'status_var') and not self.current_file:
                message = messages[self.message_index]
                self.status_var.set(message)
                self.message_index = (self.message_index + 1) % len(messages)
                self.root.after(3000, cycle_messages)
        
        self.root.after(3000, cycle_messages)
    
    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado para mejorar UX"""
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-r>', lambda e: self.refresh_file())
        self.root.bind('<Control-n>', lambda e: self.add_element())
        self.root.bind('<Delete>', lambda e: self.delete_element())
        self.root.bind('<F5>', lambda e: self.refresh_file())
        self.root.bind('<F2>', lambda e: self.edit_element())
        
        # Atajos para navegación de pestañas
        self.root.bind('<Control-1>', lambda e: self.notebook.select(0))
        self.root.bind('<Control-2>', lambda e: self.notebook.select(1))
        self.root.bind('<Control-3>', lambda e: self.notebook.select(2))
        self.root.bind('<Control-4>', lambda e: self.notebook.select(3))
    
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
        
        # Crear frame para 2 columnas
        columns_frame = tk.Frame(self.editor_scrollable_frame, bg='#0a0a0a')
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        # Frame para columna izquierda
        left_column = tk.Frame(columns_frame, bg='#0a0a0a')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Frame para columna derecha
        right_column = tk.Frame(columns_frame, bg='#0a0a0a')
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        for idx, (field, field_type) in enumerate(fields.items()):
            # Para campos grandes (markdown, content), usar todo el ancho
            if field in ['content', 'markdown']:
                column = columns_frame
            else:
                # Alternar entre columnas
                column = left_column if idx % 2 == 0 else right_column
            
            frame = tk.Frame(column, bg='#0a0a0a')
            frame.pack(fill=tk.X, pady=8)
            
            label = tk.Label(frame, text=field.upper() + ":", font=('Orbitron', 10, 'bold'), 
                           bg='#0a0a0a', fg='#ff0040')
            label.pack(anchor=tk.W)
            
            if field_type == 'text':
                entry = tk.Entry(frame, width=50, bg='#1a0a0a', fg='#ff0040', 
                               insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'textarea':
                entry = tk.Text(frame, height=4, width=50, bg='#1a0a0a', fg='#ff0040', 
                              insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'markdown':
                entry = tk.Text(frame, height=15, width=80, bg='#1a0a0a', fg='#ff0040', 
                              insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.BOTH, expand=True)
            elif field_type == 'number':
                entry = tk.Entry(frame, width=50, bg='#1a0a0a', fg='#ff0040', 
                               insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'color':
                entry = tk.Entry(frame, width=50, bg='#1a0a0a', fg='#ff0040', 
                               insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'array':
                entry = tk.Text(frame, height=3, width=50, bg='#1a0a0a', fg='#ff0040', 
                              insertbackground='#ff0040', font=('Orbitron', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'boolean':
                var = tk.StringVar(value='false')
                entry = ttk.Combobox(frame, textvariable=var, values=['true', 'false'], 
                                   state='readonly', width=47, font=('Orbitron', 10))
                entry.pack(fill=tk.X)
                self.editor_entries[field] = (var, 'boolean')
                continue
            elif field_type == 'select':
                var = tk.StringVar()
                values = ['[CREAR NUEVA...]'] + list(existing_categories) + [''] if existing_categories else ['[CREAR NUEVA...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=('Orbitron', 10))
                entry.pack(fill=tk.X)
                entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_category_selected(f, v))
                self.editor_entries[field] = (var, 'select')
                continue
            elif field_type == 'select_series':
                var = tk.StringVar()
                values = ['[CREAR NUEVA...]'] + list(existing_series) + [''] if existing_series else ['[CREAR NUEVA...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=('Orbitron', 10))
                entry.pack(fill=tk.X)
                entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_series_selected(f, v))
                self.editor_entries[field] = (var, 'select_series')
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
        
        # Categoría para secondary-projects
        if self.current_file == 'secondary-projects.json' and not element:
            cat_frame = tk.Frame(self.editor_scrollable_frame, bg='#0a0a0a')
            cat_frame.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(cat_frame, text="CATEGORÍA:", font=('Orbitron', 10, 'bold'), 
                   bg='#0a0a0a', fg='#ff0040').pack(anchor=tk.W)
            
            categories = list(self.current_data.keys()) if isinstance(self.current_data, dict) else []
            cat_var = tk.StringVar()
            cat_values = ['[CREAR NUEVA...]'] + categories if categories else ['[CREAR NUEVA...]']
            cat_combo = ttk.Combobox(cat_frame, textvariable=cat_var, values=cat_values, 
                                   state='readonly', width=47, font=('Orbitron', 10))
            cat_combo.pack(fill=tk.X)
            cat_combo.bind('<<ComboboxSelected>>', lambda e, v=cat_var: self.on_category_selected_secondary(v))
            self.editor_entries['category'] = (cat_var, 'select')
        
        # Mover los botones al final
        self.editor_button_frame.pack_forget()
        self.editor_button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Actualizar scroll region
        self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))
    
    def on_category_selected(self, field, var):
        if var.get() == '[CREAR NUEVA...]':
            new_category = simpledialog.askstring("Nueva Categoría", "Introduce el nombre de la nueva categoría:")
            if new_category:
                var.set(new_category)
    
    def on_series_selected(self, field, var):
        if var.get() == '[CREAR NUEVA...]':
            new_series = simpledialog.askstring("Nueva Serie", "Introduce el nombre de la nueva serie:")
            if new_series:
                var.set(new_series)
    
    def on_category_selected_secondary(self, var):
        if var.get() == '[CREAR NUEVA...]':
            new_category = simpledialog.askstring("Nueva Categoría", "Introduce el nombre de la nueva categoría:")
            if new_category:
                var.set(new_category)
    
    def get_fields_for_file_type(self):
        if self.current_file == 'certifications.json':
            return {
                'id': 'text',
                'name': 'text',
                'icon': 'text',
                'order': 'number',
                'issuer': 'text',
                'date': 'text',
                'credentialId': 'text',
                'badge': 'text'
            }
        elif self.current_file == 'posts.json':
            return {
                'id': 'text',
                'slug': 'text',
                'title': 'text',
                'category': 'select',
                'description': 'textarea',
                'content': 'markdown',
                'createdAt': 'text',
                'keywords': 'array',
                'readingTime': 'number',
                'wordCount': 'number',
                'featured': 'boolean',
                'published': 'boolean',
                'series': 'select_series',
                'seriesOrder': 'number',
                'seriesPartTitle': 'text'
            }
        elif self.current_file == 'projects.json':
            return {
                'id': 'text',
                'title': 'text',
                'description': 'textarea',
                'image': 'text',
                'tags': 'array',
                'color': 'color',
                'order': 'number'
            }
        elif self.current_file == 'secondary-projects.json':
            return {
                'id': 'text',
                'name': 'text',
                'description': 'textarea',
                'details': 'textarea',
                'tech': 'array',
                'link': 'text'
            }
        elif self.current_file == 'services.json':
            return {
                'id': 'text',
                'title': 'text',
                'description': 'textarea',
                'order': 'number'
            }
        return {}
    
    def save_editor(self):
        result = {}
        
        for field, (entry, field_type) in self.editor_entries.items():
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
            elif field_type in ['select', 'select_series']:
                value = entry.get().strip()
                if not value:
                    value = None
                # Para category, asegurar que no sea None
                if field == 'category' and value is None:
                    value = ''
            else:
                value = entry.get().strip()
            
            result[field] = value
        
        # Añadir campo tech vacío para projects si no existe
        if self.current_file == 'projects.json' and 'tech' not in result:
            result['tech'] = []
        
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
        self.cancel_editor()
    
    def cancel_editor(self):
        self.notebook.select(0)  # Volver al dashboard
        self.editor_mode = None
        self.editor_element = None


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()
