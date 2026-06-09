# Instrucciones Finales - Portfolio Nil Blanch

## Configuración de Base de Datos
Para habilitar el blog interactivo (likes y comentarios) con **MySQL**, añade esta variable de entorno en el panel de Cloudflare Pages:

```env
DATABASE_URL="mysql://usuario:password@tu-servidor-ionos:3306/db_name"
```

## Script Inicial SQL
Puedes ejecutar este script en tu base de datos para crear las tablas necesarias:

```sql
CREATE TABLE IF NOT EXISTS posts_meta (
  id VARCHAR(36) PRIMARY KEY,
  slug VARCHAR(255) UNIQUE NOT NULL,
  likes INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
  id VARCHAR(36) PRIMARY KEY,
  post_slug VARCHAR(255),
  author VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (post_slug) REFERENCES posts_meta(slug)
);
```

## Estructura de Contenido
- **Blog**: Los archivos markdown se pueden colocar en `src/content/posts/` (puedes crear esta carpeta y añadir un loader). Por ahora, el sistema está preparado en `src/app/blog/page.tsx`.
- **Imágenes**: Reemplaza los placeholders en `src/components/sections/projects-wall.tsx` con tus capturas reales.

## Despliegue
El proyecto está optimizado para **Vercel** o **Cloudflare Pages**. Recuerda configurar las variables de entorno en el panel de control.
