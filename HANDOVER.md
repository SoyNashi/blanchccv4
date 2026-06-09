# Instrucciones Finales - Portfolio Nil Blanch

## Configuración de Base de Datos
Para que todo el contenido (textos, proyectos, certificaciones) funcione, añade esta variable de entorno en el panel de Cloudflare Pages:

```env
DATABASE_URL="mysql://usuario:password@tu-servidor-ionos:3306/db_name"
```

## Script Inicial SQL
**¡ATENCIÓN!** Este script borrará las tablas existentes para asegurar que la estructura (incluyendo columnas como `title` o `content`) sea la correcta. Ejecútalo en la pestaña SQL de Ionos:

```sql
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts_meta;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS certifications;

-- 1. CREACIÓN DE TABLAS CORRECTAS
CREATE TABLE services (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  sort_order INT DEFAULT 0
);

CREATE TABLE projects (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  image_url VARCHAR(500) NOT NULL,
  tags JSON,
  tech JSON,
  color VARCHAR(7),
  sort_order INT DEFAULT 0
);

CREATE TABLE certifications (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  logo_url VARCHAR(500),
  sort_order INT DEFAULT 0
);

CREATE TABLE posts_meta (
  id VARCHAR(36) PRIMARY KEY,
  slug VARCHAR(255) UNIQUE NOT NULL,
  likes INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  category VARCHAR(50) DEFAULT 'novedad',
  title VARCHAR(255),
  description TEXT,
  content TEXT
);

CREATE TABLE comments (
  id VARCHAR(36) PRIMARY KEY,
  author VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  post_id VARCHAR(36),
  FOREIGN KEY (post_id) REFERENCES posts_meta(id) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS = 1;

-- 2. INSERCIÓN DE DATOS INICIALES
INSERT INTO services (id, title, description, sort_order) VALUES
('s1', 'Desarrollo Web', 'Aplicaciones web de alto rendimiento...', 1),
('s2', 'Ecommerce', 'Soluciones de comercio electrónico...', 2),
('s3', 'SEO Técnico', 'Optimización profunda desde el código...', 3),
('s4', 'Hosting & Ops', 'Infraestructura gestionada y despliegue...', 4),
('s5', 'Mantenimiento', 'Cuidado constante y evolución...', 5),
('s6', 'Consultoría', 'Asesoramiento estratégico...', 6);

INSERT INTO projects (id, title, description, image_url, tags, tech, color, sort_order) VALUES
('p1', 'Blau360', 'Digitalización a medida para PYMES...', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800', '["Product Strategy", "Full Stack Dev"]', '[{"label": "Frontend", "value": "Next.js"}, {"label": "Backend", "value": "MySQL"}]', '#0055ff', 1),
('p2', 'Bastet Project', 'Marca de ropa impulsada por valores...', 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800', '["E-commerce", "UX Design"]', '[{"label": "Storefront", "value": "Shopify"}]', '#ff3300', 2);

INSERT INTO certifications (id, name, logo_url, sort_order) VALUES
('c1', 'AWS Certified', 'https://upload.wikimedia.org/wikipedia/commons/5/5c/AWS_Simple_Icons_AWS_Cloud.svg', 1),
('c2', 'Google Cloud', 'https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg', 2);

INSERT INTO posts_meta (id, slug, title, description, category, likes, content) VALUES
('b1', 'optimizacion-nextjs-seo', 'Optimizando Next.js para SEO', 'Descripción corta...', 'creacion', 124, '# Contenido en Markdown');

-- 2. INSERCIÓN DE DATOS INICIALES

-- Servicios
INSERT IGNORE INTO services (id, title, description, sort_order) VALUES
('s1', 'Desarrollo Web', 'Aplicaciones web de alto rendimiento construidas con las tecnologías más modernas.', 1),
('s2', 'Ecommerce', 'Soluciones de comercio electrónico robustas enfocadas en la conversión.', 2),
('s3', 'SEO Técnico', 'Optimización profunda desde el código para asegurar visibilidad real.', 3),
('s4', 'Hosting & Ops', 'Infraestructura gestionada y despliegue continuo impecable.', 4),
('s5', 'Mantenimiento', 'Cuidado constante y evolución de tus sistemas digitales.', 5),
('s6', 'Consultoría', 'Asesoramiento estratégico para roadmaps técnicos de productos.', 6);

-- Proyectos
INSERT IGNORE INTO projects (id, title, description, image_url, tags, tech, color, sort_order) VALUES
('p1', 'Blau360', 'Digitalización a medida para PYMES y publicidad exterior.', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800', '["Product Strategy", "Full Stack Dev"]', '[{"label": "Frontend", "value": "Next.js"}, {"label": "Backend", "value": "MySQL"}]', '#0055ff', 1),
('p2', 'Bastet Project', 'Marca de ropa impulsada por valores y comunidad.', 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800', '["E-commerce", "UX Design"]', '[{"label": "Storefront", "value": "Shopify"}, {"label": "Automation", "value": "Klaviyo"}]', '#ff3300', 2);

-- Certificaciones
INSERT IGNORE INTO certifications (id, name, logo_url, sort_order) VALUES
('c1', 'AWS Certified', 'https://upload.wikimedia.org/wikipedia/commons/5/5c/AWS_Simple_Icons_AWS_Cloud.svg', 1),
('c2', 'Google Cloud', 'https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg', 2),
('c3', 'Meta Frontend', 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg', 3);

-- Blog (Entradas reales)
INSERT IGNORE INTO posts_meta (id, slug, title, description, category, likes) VALUES
('b1', 'optimizacion-nextjs-seo', 'Optimizando Next.js para SEO técnico extremo', 'Cómo logré un 100/100 en Lighthouse manteniendo escalabilidad.', 'creacion', 124),
('b2', 'alerta-malware-npm', 'Nueva vulnerabilidad detectada en paquetes npm', 'Análisis técnico de la última amenaza detectada en el ecosistema JS.', 'alerta', 45);
```

## Estructura de Contenido
- **Blog**: Los archivos markdown se pueden colocar en `src/content/posts/` (puedes crear esta carpeta y añadir un loader). Por ahora, el sistema está preparado en `src/app/blog/page.tsx`.
- **Imágenes**: Reemplaza los placeholders en `src/components/sections/projects-wall.tsx` con tus capturas reales.

## Despliegue
El proyecto está optimizado para **Vercel** o **Cloudflare Pages**. Recuerda configurar las variables de entorno en el panel de control.
