import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
import re

class JSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de JSON - Portfolio Nil Blanch")
        self.root.geometry("1400x900")
        
        # Configurar estilo oscuro tipo consola
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#0a0a0a')
        self.style.configure('TLabel', background='#0a0a0a', foreground='#00ff00', font=('Consolas', 10))
        self.style.configure('TButton', background='#00ff00', foreground='#000000', font=('Consolas', 10, 'bold'))
        self.style.configure('TNotebook', background='#0a0a0a')
        self.style.configure('TNotebook.Tab', background='#1a1a1a', foreground='#00ff00', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#00ff00')], foreground=[('selected', '#000000')])
        
        self.root.configure(bg='#0a0a0a')
        
        # Ruta base del proyecto
        self.base_path = Path(__file__).parent / 'src' / 'data'
        
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
        
        # Línea decorativa
        tk.Frame(header_frame, bg='#00ff00', height=2).pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="JSON EDITOR // PORTFOLIO NIL BLANCH", 
                              font=('Consolas', 18, 'bold'), bg='#0a0a0a', fg='#00ff00')
        title_label.pack(side=tk.LEFT)
        
        # Selector de archivo con estilo - botones grandes
        selector_frame = tk.Frame(main_frame, bg='#0a0a0a')
        selector_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid de botones para cada archivo
        self.file_buttons = {}
        button_grid = tk.Frame(selector_frame, bg='#0a0a0a')
        button_grid.pack(fill=tk.X)
        
        btn_style_large = {'font': ('Consolas', 12, 'bold'), 'bg': '#1a1a1a', 'fg': '#00ff00', 
                          'activebackground': '#00ff00', 'activeforeground': '#000000',
                          'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 2, 'padx': 25, 'pady': 12,
                          'highlightbackground': '#00ff00', 'highlightthickness': 1}
        
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
        
        btn_style_action = {'font': ('Consolas', 11, 'bold'), 'bg': '#00ff00', 'fg': '#000000', 
                           'activebackground': '#00cc00', 'activeforeground': '#000000',
                           'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 0, 'padx': 25, 'pady': 10}
        
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
        
        self.create_visual_view()
        self.create_text_editor()
        self.create_dashboard()
        
        # Línea decorativa
        tk.Frame(main_frame, bg='#00ff00', height=2).pack(fill=tk.X, pady=(20, 15))
        
        # Botones de acción
        action_frame = tk.Frame(main_frame, bg='#0a0a0a')
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_style = {'font': ('Consolas', 10, 'bold'), 'bg': '#00ff00', 'fg': '#000000', 
                     'activebackground': '#00cc00', 'activeforeground': '#000000',
                     'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 0}
        
        tk.Button(action_frame, text="+ ADD", command=self.add_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(action_frame, text="✏ EDIT", command=self.edit_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(action_frame, text="🗑 DELETE", command=self.delete_element, width=15, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar con estilo
        self.status_var = tk.StringVar()
        self.status_var.set("READY // SELECT A FILE TO BEGIN")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                            font=('Consolas', 9), bg='#0a0a0a', fg='#00aa00', 
                            relief=tk.FLAT, pady=10)
        status_bar.pack(fill=tk.X)
        
        # Indicador de cambios sin guardar
        self.unsaved_label = tk.Label(main_frame, text="", 
                                     font=('Consolas', 10, 'bold'), 
                                     bg='#0a0a0a', fg='#ff6600')
        self.unsaved_label.pack(fill=tk.X, pady=(5, 0))
    
    def create_visual_view(self):
        # Scrollbars
        visual_scroll_y = ttk.Scrollbar(self.visual_frame)
        visual_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        visual_scroll_x = ttk.Scrollbar(self.visual_frame, orient=tk.HORIZONTAL)
        visual_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas para vista visual
        self.visual_canvas = tk.Canvas(self.visual_frame, bg='#0a0a0a', yscrollcommand=visual_scroll_y.set, xscrollcommand=visual_scroll_x.set)
        self.visual_canvas.pack(fill=tk.BOTH, expand=True)
        
        visual_scroll_y.config(command=self.visual_canvas.yview)
        visual_scroll_x.config(command=self.visual_canvas.xview)
        
        self.visual_elements = []
        self.selected_element = None
        
        # Bind events para selección y edición
        self.visual_canvas.bind('<Button-1>', self.on_canvas_click)
        self.visual_canvas.bind('<Double-Button-1>', self.on_canvas_double_click)
    
    def create_text_editor(self):
        # Scrollbar
        text_scroll = ttk.Scrollbar(self.text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        self.text_editor = tk.Text(self.text_frame, yscrollcommand=text_scroll.set, bg='#0a0a0a', fg='#00ff00', font=('Consolas', 11), insertbackground='#00ff00')
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Detectar cambios en el editor de texto
        self.text_editor.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        self.text_editor.bind('<ButtonRelease-1>', lambda e: self.mark_unsaved())
        
        text_scroll.config(command=self.text_editor.yview)
    
    def create_dashboard(self):
        # Frame principal del dashboard
        dash_main = tk.Frame(self.dashboard_frame, bg='#0a0a0a')
        dash_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título del dashboard
        title_frame = tk.Frame(dash_main, bg='#0a0a0a')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(title_frame, text="DASHBOARD // ESTADÍSTICAS Y ACCIONES RÁPIDAS", 
                font=('Consolas', 16, 'bold'), bg='#0a0a0a', fg='#00ff00').pack(anchor=tk.W)
        
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
            card = tk.Frame(stats_grid, bg='#1a1a1a', bd=2, relief=tk.FLAT, highlightbackground='#00ff00', highlightthickness=1)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky='nsew')
            stats_grid.grid_columnconfigure(idx, weight=1)
            
            tk.Label(card, text=name.upper(), font=('Consolas', 10, 'bold'), 
                    bg='#1a1a1a', fg='#00aa00').pack(pady=(15, 5))
            tk.Label(card, text=str(count), font=('Consolas', 24, 'bold'), 
                    bg='#1a1a1a', fg='#00ff00').pack(pady=(0, 15))
            
            # Hacer la tarjeta clickeable
            card.bind('<Button-1>', lambda e, f=self.json_files[name]: self.load_specific_file(f))
        
        # Frame para acciones rápidas
        actions_frame = tk.Frame(dash_main, bg='#0a0a0a')
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(actions_frame, text="ACCIONES RÁPIDAS", 
                font=('Consolas', 14, 'bold'), bg='#0a0a0a', fg='#00ff00').pack(anchor=tk.W, pady=(0, 20))
        
        # Botones grandes para cargar archivos
        btn_grid = tk.Frame(actions_frame, bg='#0a0a0a')
        btn_grid.pack(fill=tk.BOTH, expand=True)
        
        btn_style_large = {'font': ('Consolas', 12, 'bold'), 'bg': '#00ff00', 'fg': '#000000', 
                          'activebackground': '#00cc00', 'activeforeground': '#000000',
                          'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 0, 'padx': 30, 'pady': 15}
        
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
        file_name = self.file_var.get()
        if not file_name:
            messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
            return
        
        json_file = self.json_files[file_name]
        self.load_specific_file(json_file)
    
    def refresh_file(self):
        if self.current_file:
            self.load_file()
    
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
        card_width = 380
        card_height = 220
        gap = 20
        
        for idx, post in enumerate(self.current_data):
            if idx > 0 and idx % 3 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background con gradiente simulado
            card = self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#0d1117', outline='#00ff00', width=2,
                tags=('card', f'post_{idx}')
            )
            
            # Title con wrapping
            title = post.get('title', 'Sin título')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=title,
                font=('Consolas', 11, 'bold'),
                fill='#00ff00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'post_{idx}')
            )
            
            # Category badge
            category = post.get('category', '')
            self.visual_canvas.create_rectangle(
                x_pos + 15, y_pos + 50, x_pos + 15 + len(category) * 8 + 20, y_pos + 70,
                fill='#00ff00', outline='#00ff00',
                tags=('card', f'post_{idx}')
            )
            self.visual_canvas.create_text(
                x_pos + 25, y_pos + 52,
                text=category.upper(),
                font=('Consolas', 8, 'bold'),
                fill='#000000', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Description con wrapping
            desc = post.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 80,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'post_{idx}')
            )
            
            # Date
            date = post.get('createdAt', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + card_height - 25,
                text=date,
                font=('Consolas', 8),
                fill='#008800', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Featured indicator
            if post.get('featured', False):
                self.visual_canvas.create_text(
                    x_pos + card_width - 25, y_pos + 15,
                    text="★",
                    font=('Consolas', 14),
                    fill='#ffff00', anchor='ne',
                    tags=('card', f'post_{idx}')
                )
            
            self.visual_elements.append({'type': 'post', 'index': idx, 'data': post, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        # Update scroll region
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_projects_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 320
        card_height = 200
        gap = 20
        
        for idx, project in enumerate(self.current_data):
            if idx > 0 and idx % 4 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background con color personalizado
            color = project.get('color', '#00ff00')
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#0d1117', outline=color, width=3,
                tags=('card', f'project_{idx}')
            )
            
            # Title con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=project.get('title', 'Sin título'),
                font=('Consolas', 11, 'bold'),
                fill='#00ff00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'project_{idx}')
            )
            
            # Description con wrapping
            desc = project.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 45,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
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
        card_width = 300
        card_height = 140
        gap = 15
        
        for idx, cert in enumerate(self.current_data):
            if idx > 0 and idx % 4 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#0d1117', outline='#00ff00', width=2,
                tags=('card', f'cert_{idx}')
            )
            
            # Name con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=cert.get('name', 'Sin nombre'),
                font=('Consolas', 10, 'bold'),
                fill='#00ff00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'cert_{idx}')
            )
            
            # Issuer
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 45,
                text=f"Issuer: {cert.get('issuer', '')}",
                font=('Consolas', 9),
                fill='#00aa00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'cert_{idx}')
            )
            
            # Date
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + card_height - 25,
                text=f"Date: {cert.get('date', '')}",
                font=('Consolas', 8),
                fill='#008800', anchor='nw',
                tags=('card', f'cert_{idx}')
            )
            
            # Badge indicator
            if cert.get('badge'):
                self.visual_canvas.create_text(
                    x_pos + card_width - 15, y_pos + 15,
                    text="●",
                    font=('Consolas', 12),
                    fill='#ffff00', anchor='ne',
                    tags=('card', f'cert_{idx}')
                )
            
            self.visual_elements.append({'type': 'cert', 'index': idx, 'data': cert, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_services_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 340
        card_height = 120
        gap = 15
        
        for idx, service in enumerate(self.current_data):
            if idx > 0 and idx % 3 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#0d1117', outline='#00ff00', width=2,
                tags=('card', f'service_{idx}')
            )
            
            # Title con wrapping
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 15,
                text=service.get('title', 'Sin título'),
                font=('Consolas', 11, 'bold'),
                fill='#00ff00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'service_{idx}')
            )
            
            # Description con wrapping
            desc = service.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 15, y_pos + 40,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
                width=card_width - 30,
                tags=('card', f'service_{idx}')
            )
            
            # Order indicator
            order = service.get('order', 0)
            self.visual_canvas.create_text(
                x_pos + card_width - 15, y_pos + card_height - 15,
                text=f"#{order}",
                font=('Consolas', 10, 'bold'),
                fill='#008800', anchor='se',
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
                    fill='#00ff00', outline='#00ff00',
                    tags=('header', f'cat_{category}')
                )
                self.visual_canvas.create_text(
                    x_pos + 10, y_pos + 5,
                    text=category.upper(),
                    font=('Consolas', 11, 'bold'),
                    fill='#000000', anchor='nw',
                    tags=('header', f'cat_{category}')
                )
                y_pos += 40
                
                # Projects in category
                card_width = 320
                card_height = 140
                gap = 15
                
                for idx, project in enumerate(projects):
                    if idx > 0 and idx % 3 == 0:
                        x_pos = 20
                        y_pos += card_height + gap
                    
                    # Card background
                    self.visual_canvas.create_rectangle(
                        x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                        fill='#0d1117', outline='#00ff00', width=2,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Name con wrapping
                    self.visual_canvas.create_text(
                        x_pos + 15, y_pos + 15,
                        text=project.get('name', 'Sin nombre'),
                        font=('Consolas', 10, 'bold'),
                        fill='#00ff00', anchor='nw',
                        width=card_width - 30,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Description con wrapping
                    desc = project.get('description', '')
                    self.visual_canvas.create_text(
                        x_pos + 15, y_pos + 40,
                        text=desc,
                        font=('Consolas', 9),
                        fill='#00cc00', anchor='nw',
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
                            font=('Consolas', 8),
                            fill='#00aa00', anchor='nw',
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
        
        dialog = ElementEditorDialog(self.root, "Añadir Elemento", self.current_file, self.current_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            if isinstance(self.current_data, list):
                self.current_data.append(dialog.result)
            elif isinstance(self.current_data, dict):
                # Para estructuras como secondary-projects.json
                category = dialog.result.get('category', '')
                if category in self.current_data and isinstance(self.current_data[category], list):
                    self.current_data[category].append(dialog.result)
            
            self.update_visual_view()
            self.update_text_editor()
            self.mark_unsaved()
            self.status_var.set("Elemento añadido")
    
    def edit_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        if not self.selected_element:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para editar (doble click en la tarjeta)")
            return
        
        element = self.selected_element
        
        # Manejar estructura anidada de secondary-projects
        if element.get('type') == 'secproj':
            category = element['category']
            index = element['index']
            data = element['data']
            
            if isinstance(self.current_data, dict) and category in self.current_data:
                projects = self.current_data[category]
                if isinstance(projects, list) and index < len(projects):
                    try:
                        dialog = ElementEditorDialog(self.root, "Editar Elemento", self.current_file, self.current_data, data)
                        self.root.wait_window(dialog.dialog)
                        
                        if dialog.result:
                            self.current_data[category][index] = dialog.result
                            self.update_visual_view()
                            self.update_text_editor()
                            self.mark_unsaved()
                            self.status_var.set("Elemento actualizado")
                            self.selected_element = None
                            self.visual_canvas.delete('highlight')
                    except (ValueError, IndexError):
                        messagebox.showerror("Error", "No se pudo editar el elemento")
            return
        
        # Manejar estructura normal (list)
        index = element['index']
        data = element['data']
        
        if isinstance(self.current_data, list):
            try:
                dialog = ElementEditorDialog(self.root, "Editar Elemento", self.current_file, self.current_data, data)
                self.root.wait_window(dialog.dialog)
                
                if dialog.result:
                    self.current_data[index] = dialog.result
                    self.update_visual_view()
                    self.update_text_editor()
                    self.mark_unsaved()
                    self.status_var.set("Elemento actualizado")
                    self.selected_element = None
                    self.visual_canvas.delete('highlight')
            except (ValueError, IndexError):
                messagebox.showerror("Error", "No se pudo editar el elemento")
    
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


class ElementEditorDialog:
    def __init__(self, parent, title, file_type, current_data, element=None):
        self.result = None
        self.element = element
        self.file_type = file_type
        self.current_data = current_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("800x700")
        self.dialog.configure(bg='#0d1117')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.entries = {}
        self.create_ui()
    
    def create_ui(self):
        # Scrollable frame
        canvas = tk.Canvas(self.dialog, bg='#0d1117')
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0d1117')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Campos según el tipo de archivo
        fields = self.get_fields_for_file_type()
        
        # Obtener categorías y series existentes para posts
        existing_categories = set()
        existing_series = set()
        if self.file_type == 'posts.json' and isinstance(self.current_data, list):
            for post in self.current_data:
                if 'category' in post:
                    existing_categories.add(post['category'])
                if 'series' in post and post['series']:
                    existing_series.add(post['series'])
        
        for idx, (field, field_type) in enumerate(fields.items()):
            frame = tk.Frame(scrollable_frame, bg='#0d1117')
            frame.pack(fill=tk.X, padx=15, pady=8)
            
            label = tk.Label(frame, text=field.upper() + ":", font=('Consolas', 10, 'bold'), 
                           bg='#0d1117', fg='#00ff00')
            label.pack(anchor=tk.W)
            
            if field_type == 'text':
                entry = tk.Entry(frame, width=50, bg='#1a1a1a', fg='#00ff00', 
                               insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'textarea':
                entry = tk.Text(frame, height=4, width=50, bg='#1a1a1a', fg='#00ff00', 
                              insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'markdown':
                # Editor markdown grande
                entry = tk.Text(frame, height=15, width=80, bg='#1a1a1a', fg='#00ff00', 
                              insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.BOTH, expand=True)
            elif field_type == 'number':
                entry = tk.Entry(frame, width=50, bg='#1a1a1a', fg='#00ff00', 
                               insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'color':
                entry = tk.Entry(frame, width=50, bg='#1a1a1a', fg='#00ff00', 
                               insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'array':
                entry = tk.Text(frame, height=3, width=50, bg='#1a1a1a', fg='#00ff00', 
                              insertbackground='#00ff00', font=('Consolas', 10))
                entry.pack(fill=tk.X)
            elif field_type == 'boolean':
                var = tk.StringVar(value='false')
                entry = ttk.Combobox(frame, textvariable=var, values=['true', 'false'], 
                                   state='readonly', width=47, font=('Consolas', 10))
                entry.pack(fill=tk.X)
                self.entries[field] = (var, 'boolean')
                continue
            elif field_type == 'select':
                # Selector de categorías existentes + opción de crear nueva
                var = tk.StringVar()
                values = ['[CREAR NUEVA...]'] + list(existing_categories) + [''] if existing_categories else ['[CREAR NUEVA...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=('Consolas', 10))
                entry.pack(fill=tk.X)
                entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_category_selected(f, v))
                self.entries[field] = (var, 'select')
                continue
            elif field_type == 'select_series':
                # Selector de series existentes + opción de crear nueva
                var = tk.StringVar()
                values = ['[CREAR NUEVA...]'] + list(existing_series) + [''] if existing_series else ['[CREAR NUEVA...]', '']
                entry = ttk.Combobox(frame, textvariable=var, values=values, 
                                   state='readonly', width=47, font=('Consolas', 10))
                entry.pack(fill=tk.X)
                entry.bind('<<ComboboxSelected>>', lambda e, f=field, v=var: self.on_series_selected(f, v))
                self.entries[field] = (var, 'select_series')
                continue
            
            # Valor por defecto si estamos editando
            if self.element and field in self.element:
                value = self.element[field]
                if field_type in ['textarea', 'array', 'markdown']:
                    if isinstance(value, list):
                        entry.insert(1.0, ', '.join(str(v) for v in value))
                    else:
                        entry.insert(1.0, str(value))
                else:
                    entry.insert(0, str(value))
            
            self.entries[field] = (entry, field_type)
        
        # Categoría para secondary-projects
        if self.file_type == 'secondary-projects.json' and not self.element:
            cat_frame = tk.Frame(scrollable_frame, bg='#0d1117')
            cat_frame.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(cat_frame, text="CATEGORÍA:", font=('Consolas', 10, 'bold'), 
                   bg='#0d1117', fg='#00ff00').pack(anchor=tk.W)
            
            categories = list(self.current_data.keys()) if isinstance(self.current_data, dict) else []
            cat_var = tk.StringVar()
            cat_values = ['[CREAR NUEVA...]'] + categories if categories else ['[CREAR NUEVA...]']
            cat_combo = ttk.Combobox(cat_frame, textvariable=cat_var, values=cat_values, 
                                   state='readonly', width=47, font=('Consolas', 10))
            cat_combo.pack(fill=tk.X)
            cat_combo.bind('<<ComboboxSelected>>', lambda e, v=cat_var: self.on_category_selected_secondary(v))
            self.entries['category'] = (cat_var, 'select')
        
        # Botones
        button_frame = tk.Frame(scrollable_frame, bg='#0d1117')
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_style = {'font': ('Consolas', 10, 'bold'), 'bg': '#00ff00', 'fg': '#000000', 
                     'activebackground': '#00cc00', 'activeforeground': '#000000',
                     'relief': tk.FLAT, 'cursor': 'hand2', 'bd': 0, 'padx': 20, 'pady': 8}
        
        tk.Button(button_frame, text="SAVE", command=self.save, **btn_style).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="CANCEL", command=self.cancel, **btn_style).pack(side=tk.LEFT)
    
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
        if self.file_type == 'certifications.json':
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
        elif self.file_type == 'posts.json':
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
        elif self.file_type == 'projects.json':
            return {
                'id': 'text',
                'title': 'text',
                'description': 'textarea',
                'image': 'text',
                'tags': 'array',
                'color': 'color',
                'order': 'number'
            }
        elif self.file_type == 'secondary-projects.json':
            return {
                'id': 'text',
                'name': 'text',
                'description': 'textarea',
                'details': 'textarea',
                'tech': 'array',
                'link': 'text'
            }
        elif self.file_type == 'services.json':
            return {
                'id': 'text',
                'title': 'text',
                'description': 'textarea',
                'order': 'number'
            }
        return {}
    
    def save(self):
        result = {}
        
        for field, (entry, field_type) in self.entries.items():
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
            else:
                value = entry.get().strip()
            
            result[field] = value
        
        # Añadir campo tech vacío para projects si no existe
        if self.file_type == 'projects.json' and 'tech' not in result:
            result['tech'] = []
        
        # Para posts, asegurar que los campos nuevos tengan valores por defecto
        if self.file_type == 'posts.json':
            if 'keywords' not in result or not result['keywords']:
                result['keywords'] = []
            if 'readingTime' not in result:
                result['readingTime'] = 0
            if 'wordCount' not in result:
                result['wordCount'] = 0
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
        
        self.result = result
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()
