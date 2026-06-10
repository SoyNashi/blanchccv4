import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from pathlib import Path

class DataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Datos - Blanch.cc")
        self.root.geometry("1000x700")
        
        self.base_path = Path(__file__).parent / "src" / "data"
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña para Projects
        self.projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_frame, text='Projects')
        self.create_projects_tab()
        
        # Pestaña para Services
        self.services_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.services_frame, text='Services')
        self.create_services_tab()
        
        # Pestaña para Certifications
        self.certifications_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.certifications_frame, text='Certifications')
        self.create_certifications_tab()
        
        # Pestaña para Posts
        self.posts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.posts_frame, text='Posts')
        self.create_posts_tab()
        
        # Cargar datos iniciales
        self.load_projects()
        self.load_services()
        self.load_certifications()
        self.load_posts()
    
    def create_projects_tab(self):
        # Botones
        btn_frame = ttk.Frame(self.projects_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Añadir Project', command=self.add_project).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Guardar', command=self.save_projects).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Eliminar Seleccionado', command=self.delete_project).pack(side='left', padx=5)
        
        # Treeview
        self.projects_tree = ttk.Treeview(self.projects_frame, columns=('id', 'title', 'description', 'order'), show='headings')
        self.projects_tree.heading('id', text='ID')
        self.projects_tree.heading('title', text='Title')
        self.projects_tree.heading('description', text='Description')
        self.projects_tree.heading('order', text='Order')
        
        self.projects_tree.column('id', width=50)
        self.projects_tree.column('title', width=200)
        self.projects_tree.column('description', width=400)
        self.projects_tree.column('order', width=50)
        
        self.projects_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.projects_tree.bind('<<TreeviewSelect>>', self.on_project_select)
        
        # Formulario de edición
        self.project_edit_frame = ttk.LabelFrame(self.projects_frame, text='Editar Project')
        self.project_edit_frame.pack(fill='x', padx=5, pady=5)
        
        self.create_entry(self.project_edit_frame, 'ID:', 'project_id', 0)
        self.create_entry(self.project_edit_frame, 'Title:', 'project_title', 1)
        self.create_text(self.project_edit_frame, 'Description:', 'project_description', 2)
        self.create_entry(self.project_edit_frame, 'Image URL:', 'project_image', 3)
        self.create_entry(self.project_edit_frame, 'Color:', 'project_color', 4)
        self.create_entry(self.project_edit_frame, 'Order:', 'project_order', 5)
        
        ttk.Button(self.project_edit_frame, text='Actualizar', command=self.update_project).grid(row=6, column=1, pady=5)
    
    def create_services_tab(self):
        btn_frame = ttk.Frame(self.services_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Añadir Service', command=self.add_service).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Guardar', command=self.save_services).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Eliminar Seleccionado', command=self.delete_service).pack(side='left', padx=5)
        
        self.services_tree = ttk.Treeview(self.services_frame, columns=('id', 'title', 'description', 'order'), show='headings')
        self.services_tree.heading('id', text='ID')
        self.services_tree.heading('title', text='Title')
        self.services_tree.heading('description', text='Description')
        self.services_tree.heading('order', text='Order')
        
        self.services_tree.column('id', width=50)
        self.services_tree.column('title', width=200)
        self.services_tree.column('description', width=400)
        self.services_tree.column('order', width=50)
        
        self.services_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.services_tree.bind('<<TreeviewSelect>>', self.on_service_select)
        
        self.service_edit_frame = ttk.LabelFrame(self.services_frame, text='Editar Service')
        self.service_edit_frame.pack(fill='x', padx=5, pady=5)
        
        self.create_entry(self.service_edit_frame, 'ID:', 'service_id', 0)
        self.create_entry(self.service_edit_frame, 'Title:', 'service_title', 1)
        self.create_text(self.service_edit_frame, 'Description:', 'service_description', 2)
        self.create_entry(self.service_edit_frame, 'Order:', 'service_order', 3)
        
        ttk.Button(self.service_edit_frame, text='Actualizar', command=self.update_service).grid(row=4, column=1, pady=5)
    
    def create_certifications_tab(self):
        btn_frame = ttk.Frame(self.certifications_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Añadir Certification', command=self.add_certification).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Guardar', command=self.save_certifications).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Eliminar Seleccionado', command=self.delete_certification).pack(side='left', padx=5)
        
        self.certifications_tree = ttk.Treeview(self.certifications_frame, columns=('id', 'name', 'logo', 'order'), show='headings')
        self.certifications_tree.heading('id', text='ID')
        self.certifications_tree.heading('name', text='Name')
        self.certifications_tree.heading('logo', text='Logo')
        self.certifications_tree.heading('order', text='Order')
        
        self.certifications_tree.column('id', width=50)
        self.certifications_tree.column('name', width=200)
        self.certifications_tree.column('logo', width=300)
        self.certifications_tree.column('order', width=50)
        
        self.certifications_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.certifications_tree.bind('<<TreeviewSelect>>', self.on_certification_select)
        
        self.certification_edit_frame = ttk.LabelFrame(self.certifications_frame, text='Editar Certification')
        self.certification_edit_frame.pack(fill='x', padx=5, pady=5)
        
        self.create_entry(self.certification_edit_frame, 'ID:', 'cert_id', 0)
        self.create_entry(self.certification_edit_frame, 'Name:', 'cert_name', 1)
        self.create_entry(self.certification_edit_frame, 'Logo URL:', 'cert_logo', 2)
        self.create_entry(self.certification_edit_frame, 'Order:', 'cert_order', 3)
        
        ttk.Button(self.certification_edit_frame, text='Actualizar', command=self.update_certification).grid(row=4, column=1, pady=5)
    
    def create_posts_tab(self):
        btn_frame = ttk.Frame(self.posts_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Añadir Post', command=self.add_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Guardar', command=self.save_posts).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Eliminar Seleccionado', command=self.delete_post).pack(side='left', padx=5)
        
        self.posts_tree = ttk.Treeview(self.posts_frame, columns=('slug', 'title', 'category'), show='headings')
        self.posts_tree.heading('slug', text='Slug')
        self.posts_tree.heading('title', text='Title')
        self.posts_tree.heading('category', text='Category')
        
        self.posts_tree.column('slug', width=200)
        self.posts_tree.column('title', width=300)
        self.posts_tree.column('category', width=100)
        
        self.posts_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.posts_tree.bind('<<TreeviewSelect>>', self.on_post_select)
        
        self.post_edit_frame = ttk.LabelFrame(self.posts_frame, text='Editar Post')
        self.post_edit_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.create_entry(self.post_edit_frame, 'Slug:', 'post_slug', 0)
        self.create_entry(self.post_edit_frame, 'Title:', 'post_title', 1)
        self.create_entry(self.post_edit_frame, 'Category:', 'post_category', 2)
        self.create_entry(self.post_edit_frame, 'Description:', 'post_description', 3)
        self.create_entry(self.post_edit_frame, 'Created At:', 'post_created', 4)
        self.create_entry(self.post_edit_frame, 'Likes:', 'post_likes', 5)
        self.create_text(self.post_edit_frame, 'Content:', 'post_content', 6)
        
        ttk.Button(self.post_edit_frame, text='Actualizar', command=self.update_post).grid(row=7, column=1, pady=5)
    
    def create_entry(self, parent, label, attr_name, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, padx=5, pady=2, sticky='e')
        entry = ttk.Entry(parent, width=60)
        entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        setattr(self, attr_name, entry)
    
    def create_text(self, parent, label, attr_name, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, padx=5, pady=2, sticky='ne')
        text = tk.Text(parent, width=60, height=4)
        text.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        setattr(self, attr_name, text)
    
    # Projects methods
    def load_projects(self):
        self.projects_data = []
        try:
            with open(self.base_path / 'projects.json', 'r') as f:
                self.projects_data = json.load(f)
        except FileNotFoundError:
            pass
        
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        for project in self.projects_data:
            self.projects_tree.insert('', 'end', values=(
                project.get('id', ''),
                project.get('title', ''),
                project.get('description', '')[:50] + '...' if len(project.get('description', '')) > 50 else project.get('description', ''),
                project.get('order', '')
            ))
    
    def add_project(self):
        new_project = {
            'id': str(len(self.projects_data) + 1),
            'title': 'New Project',
            'description': '',
            'image': '',
            'tags': [],
            'tech': [],
            'color': '#000000',
            'order': len(self.projects_data) + 1
        }
        self.projects_data.append(new_project)
        self.load_projects()
    
    def update_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            return
        
        item = self.projects_tree.item(selected[0])
        idx = self.projects_tree.index(selected[0])
        
        self.projects_data[idx] = {
            'id': self.project_id.get(),
            'title': self.project_title.get(),
            'description': self.project_description.get(1.0, tk.END).strip(),
            'image': self.project_image.get(),
            'tags': [],
            'tech': [],
            'color': self.project_color.get(),
            'order': int(self.project_order.get())
        }
        self.load_projects()
    
    def delete_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            return
        
        idx = self.projects_tree.index(selected[0])
        del self.projects_data[idx]
        self.load_projects()
    
    def save_projects(self):
        with open(self.base_path / 'projects.json', 'w') as f:
            json.dump(self.projects_data, f, indent=2)
        messagebox.showinfo('Éxito', 'Projects guardados correctamente')
    
    def on_project_select(self, event):
        selected = self.projects_tree.selection()
        if not selected:
            return
        
        item = self.projects_tree.item(selected[0])
        idx = self.projects_tree.index(selected[0])
        project = self.projects_data[idx]
        
        self.project_id.delete(0, tk.END)
        self.project_id.insert(0, project.get('id', ''))
        
        self.project_title.delete(0, tk.END)
        self.project_title.insert(0, project.get('title', ''))
        
        self.project_description.delete(1.0, tk.END)
        self.project_description.insert(1.0, project.get('description', ''))
        
        self.project_image.delete(0, tk.END)
        self.project_image.insert(0, project.get('image', ''))
        
        self.project_color.delete(0, tk.END)
        self.project_color.insert(0, project.get('color', ''))
        
        self.project_order.delete(0, tk.END)
        self.project_order.insert(0, str(project.get('order', '')))
    
    # Services methods
    def load_services(self):
        self.services_data = []
        try:
            with open(self.base_path / 'services.json', 'r') as f:
                self.services_data = json.load(f)
        except FileNotFoundError:
            pass
        
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        for service in self.services_data:
            self.services_tree.insert('', 'end', values=(
                service.get('id', ''),
                service.get('title', ''),
                service.get('description', '')[:50] + '...' if len(service.get('description', '')) > 50 else service.get('description', ''),
                service.get('order', '')
            ))
    
    def add_service(self):
        new_service = {
            'id': str(len(self.services_data) + 1),
            'title': 'New Service',
            'description': '',
            'order': len(self.services_data) + 1
        }
        self.services_data.append(new_service)
        self.load_services()
    
    def update_service(self):
        selected = self.services_tree.selection()
        if not selected:
            return
        
        idx = self.services_tree.index(selected[0])
        self.services_data[idx] = {
            'id': self.service_id.get(),
            'title': self.service_title.get(),
            'description': self.service_description.get(1.0, tk.END).strip(),
            'order': int(self.service_order.get())
        }
        self.load_services()
    
    def delete_service(self):
        selected = self.services_tree.selection()
        if not selected:
            return
        
        idx = self.services_tree.index(selected[0])
        del self.services_data[idx]
        self.load_services()
    
    def save_services(self):
        with open(self.base_path / 'services.json', 'w') as f:
            json.dump(self.services_data, f, indent=2)
        messagebox.showinfo('Éxito', 'Services guardados correctamente')
    
    def on_service_select(self, event):
        selected = self.services_tree.selection()
        if not selected:
            return
        
        idx = self.services_tree.index(selected[0])
        service = self.services_data[idx]
        
        self.service_id.delete(0, tk.END)
        self.service_id.insert(0, service.get('id', ''))
        
        self.service_title.delete(0, tk.END)
        self.service_title.insert(0, service.get('title', ''))
        
        self.service_description.delete(1.0, tk.END)
        self.service_description.insert(1.0, service.get('description', ''))
        
        self.service_order.delete(0, tk.END)
        self.service_order.insert(0, str(service.get('order', '')))
    
    # Certifications methods
    def load_certifications(self):
        self.certifications_data = []
        try:
            with open(self.base_path / 'certifications.json', 'r') as f:
                self.certifications_data = json.load(f)
        except FileNotFoundError:
            pass
        
        for item in self.certifications_tree.get_children():
            self.certifications_tree.delete(item)
        
        for cert in self.certifications_data:
            self.certifications_tree.insert('', 'end', values=(
                cert.get('id', ''),
                cert.get('name', ''),
                cert.get('logo', ''),
                cert.get('order', '')
            ))
    
    def add_certification(self):
        new_cert = {
            'id': str(len(self.certifications_data) + 1),
            'name': 'New Certification',
            'logo': '',
            'order': len(self.certifications_data) + 1
        }
        self.certifications_data.append(new_cert)
        self.load_certifications()
    
    def update_certification(self):
        selected = self.certifications_tree.selection()
        if not selected:
            return
        
        idx = self.certifications_tree.index(selected[0])
        self.certifications_data[idx] = {
            'id': self.cert_id.get(),
            'name': self.cert_name.get(),
            'logo': self.cert_logo.get(),
            'order': int(self.cert_order.get())
        }
        self.load_certifications()
    
    def delete_certification(self):
        selected = self.certifications_tree.selection()
        if not selected:
            return
        
        idx = self.certifications_tree.index(selected[0])
        del self.certifications_data[idx]
        self.load_certifications()
    
    def save_certifications(self):
        with open(self.base_path / 'certifications.json', 'w') as f:
            json.dump(self.certifications_data, f, indent=2)
        messagebox.showinfo('Éxito', 'Certifications guardados correctamente')
    
    def on_certification_select(self, event):
        selected = self.certifications_tree.selection()
        if not selected:
            return
        
        idx = self.certifications_tree.index(selected[0])
        cert = self.certifications_data[idx]
        
        self.cert_id.delete(0, tk.END)
        self.cert_id.insert(0, cert.get('id', ''))
        
        self.cert_name.delete(0, tk.END)
        self.cert_name.insert(0, cert.get('name', ''))
        
        self.cert_logo.delete(0, tk.END)
        self.cert_logo.insert(0, cert.get('logo', ''))
        
        self.cert_order.delete(0, tk.END)
        self.cert_order.insert(0, str(cert.get('order', '')))
    
    # Posts methods
    def load_posts(self):
        self.posts_data = {}
        posts_dir = self.base_path / 'posts'
        
        if not posts_dir.exists():
            return
        
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
        
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                filepath = posts_dir / filename
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Parse frontmatter
                frontmatter = {}
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 2:
                        import yaml
                        try:
                            frontmatter = yaml.safe_load(parts[1])
                        except:
                            pass
                
                slug = filename.replace('.md', '')
                self.posts_data[slug] = {
                    'filename': filename,
                    'frontmatter': frontmatter,
                    'content': content
                }
                
                self.posts_tree.insert('', 'end', values=(
                    slug,
                    frontmatter.get('title', ''),
                    frontmatter.get('category', '')
                ))
    
    def add_post(self):
        slug = f"new-post-{len(self.posts_data) + 1}"
        content = f"""---
title: "New Post"
category: "novedad"
description: ""
createdAt: "2024-01-01T00:00:00Z"
likes: 0
---

Contenido del post...
"""
        
        posts_dir = self.base_path / 'posts'
        with open(posts_dir / f"{slug}.md", 'w') as f:
            f.write(content)
        
        self.load_posts()
    
    def update_post(self):
        selected = self.posts_tree.selection()
        if not selected:
            return
        
        item = self.posts_tree.item(selected[0])
        slug = item['values'][0]
        
        content = f"""---
title: "{self.post_title.get()}"
category: "{self.post_category.get()}"
description: "{self.post_description.get()}"
createdAt: "{self.post_created.get()}"
likes: {self.post_likes.get()}
---

{self.post_content.get(1.0, tk.END).strip()}
"""
        
        posts_dir = self.base_path / 'posts'
        with open(posts_dir / f"{slug}.md", 'w') as f:
            f.write(content)
        
        self.load_posts()
    
    def delete_post(self):
        selected = self.posts_tree.selection()
        if not selected:
            return
        
        item = self.posts_tree.item(selected[0])
        slug = item['values'][0]
        
        posts_dir = self.base_path / 'posts'
        os.remove(posts_dir / f"{slug}.md")
        
        self.load_posts()
    
    def save_posts(self):
        messagebox.showinfo('Éxito', 'Posts guardados correctamente (los cambios se guardan automáticamente al actualizar)')
    
    def on_post_select(self, event):
        selected = self.posts_tree.selection()
        if not selected:
            return
        
        item = self.posts_tree.item(selected[0])
        slug = item['values'][0]
        
        post_data = self.posts_data.get(slug, {})
        frontmatter = post_data.get('frontmatter', {})
        
        self.post_slug.delete(0, tk.END)
        self.post_slug.insert(0, slug)
        
        self.post_title.delete(0, tk.END)
        self.post_title.insert(0, frontmatter.get('title', ''))
        
        self.post_category.delete(0, tk.END)
        self.post_category.insert(0, frontmatter.get('category', ''))
        
        self.post_description.delete(0, tk.END)
        self.post_description.insert(0, frontmatter.get('description', ''))
        
        self.post_created.delete(0, tk.END)
        self.post_created.insert(0, frontmatter.get('createdAt', ''))
        
        self.post_likes.delete(0, tk.END)
        self.post_likes.insert(0, str(frontmatter.get('likes', 0)))
        
        self.post_content.delete(1.0, tk.END)
        # Extract content after frontmatter
        content = post_data.get('content', '')
        if '---' in content:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                self.post_content.insert(1.0, parts[2].strip())
            else:
                self.post_content.insert(1.0, content)
        else:
            self.post_content.insert(1.0, content)

if __name__ == '__main__':
    root = tk.Tk()
    app = DataEditor(root)
    root.mainloop()
