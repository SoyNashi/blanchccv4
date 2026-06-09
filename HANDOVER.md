# Instrucciones Finales - Portfolio Nil Blanch

## Configuración de Base de Datos
Para habilitar el blog interactivo (likes y comentarios), debes añadir la siguiente variable de entorno:

```env
DATABASE_URL="postgres://usuario:password@tu-servidor-ionos:5432/db_name"
```

## Script Inicial SQL
Puedes ejecutar este script en tu base de datos para crear las tablas necesarias:

```sql
CREATE TABLE posts_meta (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  likes INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_slug TEXT REFERENCES posts_meta(slug),
  author TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Estructura de Contenido
- **Blog**: Los archivos markdown se pueden colocar en `src/content/posts/` (puedes crear esta carpeta y añadir un loader). Por ahora, el sistema está preparado en `src/app/blog/page.tsx`.
- **Imágenes**: Reemplaza los placeholders en `src/components/sections/projects-wall.tsx` con tus capturas reales.

## Despliegue
El proyecto está optimizado para **Vercel** o **Cloudflare Pages**. Recuerda configurar las variables de entorno en el panel de control.
