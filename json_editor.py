import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        
        self.create_ui()
    
    def create_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Editor de JSON - Portfolio Nil Blanch", font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Selector de archivo
        selector_frame = ttk.Frame(main_frame)
        selector_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(selector_frame, text="Seleccionar archivo:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.file_var = tk.StringVar()
        file_combo = ttk.Combobox(selector_frame, textvariable=self.file_var, values=list(self.json_files.keys()), state='readonly', width=25, font=('Arial', 10))
        file_combo.pack(side=tk.LEFT, padx=(0, 10))
        file_combo.bind('<<ComboboxSelected>>', self.load_file)
        
        load_btn = ttk.Button(selector_frame, text="Cargar", command=self.load_file, width=10)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = ttk.Button(selector_frame, text="Guardar", command=self.save_file, width=10)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = ttk.Button(selector_frame, text="Recargar", command=self.refresh_file, width=10)
        refresh_btn.pack(side=tk.LEFT)
        
        # Notebook para diferentes vistas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Vista visual por tipo de JSON
        self.visual_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visual_frame, text='Vista Visual')
        
        # Editor de texto para JSON raw
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='JSON Raw')
        
        self.create_visual_view()
        self.create_text_editor()
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(action_frame, text="+ Añadir", command=self.add_element, width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="✏ Editar", command=self.edit_element, width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🗑 Eliminar", command=self.delete_element, width=12).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Listo - Selecciona un archivo para comenzar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, font=('Arial', 9))
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
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
        
        text_scroll.config(command=self.text_editor.yview)
    
    def load_file(self, event=None):
        file_name = self.file_var.get()
        if not file_name:
            messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
            return
        
        json_file = self.json_files[file_name]
        file_path = self.base_path / json_file
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_data = json.load(f)
                self.current_file = json_file
            
            self.update_visual_view()
            self.update_text_editor()
            self.status_var.set(f"Archivo cargado: {json_file}")
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {file_path}")
            self.status_var.set("Error: Archivo no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error al decodificar JSON: {file_path}")
            self.status_var.set("Error: JSON inválido")
    
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
        card_width = 350
        card_height = 200
        gap = 20
        
        for idx, post in enumerate(self.current_data):
            if idx > 0 and idx % 3 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            card = self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a1a1a', outline='#00ff00', width=2,
                tags=('card', f'post_{idx}')
            )
            
            # Title
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 15,
                text=post.get('title', 'Sin título'),
                font=('Consolas', 12, 'bold'),
                fill='#00ff00', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Category
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 45,
                text=f"Category: {post.get('category', '')}",
                font=('Consolas', 9),
                fill='#00aa00', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Description (truncated)
            desc = post.get('description', '')[:80] + '...' if len(post.get('description', '')) > 80 else post.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 65,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            # Date
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + card_height - 25,
                text=post.get('createdAt', ''),
                font=('Consolas', 8),
                fill='#008800', anchor='nw',
                tags=('card', f'post_{idx}')
            )
            
            self.visual_elements.append({'type': 'post', 'index': idx, 'data': post, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        # Update scroll region
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_projects_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 300
        card_height = 180
        gap = 20
        
        for idx, project in enumerate(self.current_data):
            if idx > 0 and idx % 4 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            color = project.get('color', '#00ff00')
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a1a1a', outline=color, width=3,
                tags=('card', f'project_{idx}')
            )
            
            # Title
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 15,
                text=project.get('title', 'Sin título'),
                font=('Consolas', 11, 'bold'),
                fill='#00ff00', anchor='nw',
                tags=('card', f'project_{idx}')
            )
            
            # Description (truncated)
            desc = project.get('description', '')[:60] + '...' if len(project.get('description', '')) > 60 else project.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 40,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
                tags=('card', f'project_{idx}')
            )
            
            # Tags
            tags = project.get('tags', [])
            if tags:
                tags_text = ', '.join(tags[:3])
                self.visual_canvas.create_text(
                    x_pos + 10, y_pos + card_height - 30,
                    text=tags_text,
                    font=('Consolas', 8),
                    fill='#00aa00', anchor='nw',
                    tags=('card', f'project_{idx}')
                )
            
            self.visual_elements.append({'type': 'project', 'index': idx, 'data': project, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_certifications_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 280
        card_height = 120
        gap = 15
        
        for idx, cert in enumerate(self.current_data):
            if idx > 0 and idx % 4 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a1a1a', outline='#00ff00', width=2,
                tags=('card', f'cert_{idx}')
            )
            
            # Name
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 15,
                text=cert.get('name', 'Sin nombre'),
                font=('Consolas', 10, 'bold'),
                fill='#00ff00', anchor='nw',
                tags=('card', f'cert_{idx}')
            )
            
            # Issuer
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 40,
                text=f"Issuer: {cert.get('issuer', '')}",
                font=('Consolas', 9),
                fill='#00aa00', anchor='nw',
                tags=('card', f'cert_{idx}')
            )
            
            # Date
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + card_height - 25,
                text=f"Date: {cert.get('date', '')}",
                font=('Consolas', 8),
                fill='#008800', anchor='nw',
                tags=('card', f'cert_{idx}')
            )
            
            self.visual_elements.append({'type': 'cert', 'index': idx, 'data': cert, 'x': x_pos, 'y': y_pos, 'width': card_width, 'height': card_height})
            x_pos += card_width + gap
        
        self.visual_canvas.configure(scrollregion=self.visual_canvas.bbox('all'))
    
    def create_services_view(self):
        y_pos = 20
        x_pos = 20
        card_width = 320
        card_height = 100
        gap = 15
        
        for idx, service in enumerate(self.current_data):
            if idx > 0 and idx % 3 == 0:
                x_pos = 20
                y_pos += card_height + gap
            
            # Card background
            self.visual_canvas.create_rectangle(
                x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                fill='#1a1a1a', outline='#00ff00', width=2,
                tags=('card', f'service_{idx}')
            )
            
            # Title
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 15,
                text=service.get('title', 'Sin título'),
                font=('Consolas', 11, 'bold'),
                fill='#00ff00', anchor='nw',
                tags=('card', f'service_{idx}')
            )
            
            # Description (truncated)
            desc = service.get('description', '')[:70] + '...' if len(service.get('description', '')) > 70 else service.get('description', '')
            self.visual_canvas.create_text(
                x_pos + 10, y_pos + 40,
                text=desc,
                font=('Consolas', 9),
                fill='#00cc00', anchor='nw',
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
                # Category header
                self.visual_canvas.create_text(
                    x_pos, y_pos,
                    text=category,
                    font=('Consolas', 14, 'bold'),
                    fill='#00ff00', anchor='nw'
                )
                y_pos += 30
                
                # Projects in category
                card_width = 300
                card_height = 120
                gap = 15
                
                for idx, project in enumerate(projects):
                    if idx > 0 and idx % 3 == 0:
                        x_pos = 20
                        y_pos += card_height + gap
                    
                    # Card background
                    self.visual_canvas.create_rectangle(
                        x_pos, y_pos, x_pos + card_width, y_pos + card_height,
                        fill='#1a1a1a', outline='#00ff00', width=2,
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Name
                    self.visual_canvas.create_text(
                        x_pos + 10, y_pos + 15,
                        text=project.get('name', 'Sin nombre'),
                        font=('Consolas', 10, 'bold'),
                        fill='#00ff00', anchor='nw',
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Description (truncated)
                    desc = project.get('description', '')[:60] + '...' if len(project.get('description', '')) > 60 else project.get('description', '')
                    self.visual_canvas.create_text(
                        x_pos + 10, y_pos + 40,
                        text=desc,
                        font=('Consolas', 9),
                        fill='#00cc00', anchor='nw',
                        tags=('card', f'secproj_{category}_{idx}')
                    )
                    
                    # Tech
                    tech = project.get('tech', [])
                    if tech:
                        tech_text = ', '.join(tech[:2])
                        self.visual_canvas.create_text(
                            x_pos + 10, y_pos + card_height - 25,
                            text=tech_text,
                            font=('Consolas', 8),
                            fill='#00aa00', anchor='nw',
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
        x, y = self.canvasx = event.x, event.y
        clicked_items = self.visual_canvas.find_overlapping(x, y, x+1, y+1)
        
        if clicked_items:
            # Obtener tags del elemento clickeado
            tags = self.visual_canvas.gettags(clicked_items[0])
            if 'card' in tags:
                # Extraer índice del elemento
                for tag in tags:
                    if '_' in tag:
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
            
            self.update_treeview()
            self.update_text_editor()
            self.status_var.set("Elemento añadido")
    
    def edit_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para editar")
            return
        
        item = self.tree.item(selected[0])
        index = item['text']
        
        if isinstance(self.current_data, list):
            try:
                element = self.current_data[int(index)]
                dialog = ElementEditorDialog(self.root, "Editar Elemento", self.current_file, self.current_data, element)
                self.root.wait_window(dialog.dialog)
                
                if dialog.result:
                    self.current_data[int(index)] = dialog.result
                    self.update_treeview()
                    self.update_text_editor()
                    self.status_var.set("Elemento actualizado")
            except (ValueError, IndexError):
                messagebox.showerror("Error", "No se pudo editar el elemento")
    
    def delete_element(self):
        if not self.current_data:
            messagebox.showwarning("Advertencia", "Carga un archivo primero")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este elemento?"):
            item = self.tree.item(selected[0])
            index = item['text']
            
            if isinstance(self.current_data, list):
                try:
                    del self.current_data[int(index)]
                    self.update_treeview()
                    self.update_text_editor()
                    self.status_var.set("Elemento eliminado")
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
            
            messagebox.showinfo("Éxito", f"Archivo guardado: {self.current_file}")
            self.status_var.set(f"Archivo guardado: {self.current_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar archivo: {str(e)}")
            self.status_var.set("Error al guardar archivo")


class ElementEditorDialog:
    def __init__(self, parent, title, file_type, current_data, element=None):
        self.result = None
        self.element = element
        self.file_type = file_type
        self.current_data = current_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='#1a1a1a')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.entries = {}
        self.create_ui()
    
    def create_ui(self):
        # Scrollable frame
        canvas = tk.Canvas(self.dialog, bg='#1a1a1a')
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
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
        
        for idx, (field, field_type) in enumerate(fields.items()):
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            label = ttk.Label(frame, text=field + ":")
            label.pack(anchor=tk.W)
            
            if field_type == 'text':
                entry = ttk.Entry(frame, width=50)
                entry.pack(fill=tk.X)
            elif field_type == 'textarea':
                entry = tk.Text(frame, height=4, width=50, bg='#f5f5f5', fg='#000000', insertbackground='#000000')
                entry.pack(fill=tk.X)
            elif field_type == 'markdown':
                # Editor markdown grande
                entry = tk.Text(frame, height=15, width=80, bg='#f5f5f5', fg='#000000', insertbackground='#000000', font=('Consolas', 10))
                entry.pack(fill=tk.BOTH, expand=True)
            elif field_type == 'number':
                entry = ttk.Entry(frame, width=50)
                entry.pack(fill=tk.X)
            elif field_type == 'color':
                entry = ttk.Entry(frame, width=50)
                entry.pack(fill=tk.X)
            elif field_type == 'array':
                entry = tk.Text(frame, height=3, width=50, bg='#f5f5f5', fg='#000000', insertbackground='#000000')
                entry.pack(fill=tk.X)
            
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
            cat_frame = ttk.Frame(scrollable_frame)
            cat_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(cat_frame, text="Categoría:").pack(anchor=tk.W)
            
            categories = list(self.current_data.keys()) if isinstance(self.current_data, dict) else []
            cat_var = tk.StringVar()
            cat_combo = ttk.Combobox(cat_frame, textvariable=cat_var, values=categories, state='readonly', width=47)
            cat_combo.pack(fill=tk.X)
            self.entries['category'] = (cat_combo, 'select')
        
        # Botones
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=self.save).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT)
    
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
                'category': 'text',
                'description': 'textarea',
                'content': 'markdown',
                'createdAt': 'text'
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
            else:
                value = entry.get().strip()
            
            result[field] = value
        
        # Añadir campo tech vacío para projects si no existe
        if self.file_type == 'projects.json' and 'tech' not in result:
            result['tech'] = []
        
        self.result = result
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()
