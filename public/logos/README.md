# Logos del hero

Coloca aquí los logotipos cuadrados en PNG, SVG o WebP, preferiblemente con fondo transparente.
Cada archivo debe añadirse también a `src/data/hero-logos.json` con esta estructura:

```json
{
  "image": "/logos/nombre-del-logo.svg",
  "title": "Nombre",
  "href": "https://web-del-proyecto.example"
}
```

- `image`: ruta pública dentro de esta carpeta.
- `title`: nombre accesible del proyecto o colaborador.
- `href`: destino externo, página del proyecto o artículo del blog.

El muro distribuye automáticamente las entradas del JSON en tres columnas. No es necesario modificar DriftWall al añadir logotipos.
Los SVG de ejemplo son marcas tipográficas provisionales: sustitúyelos por los logos oficiales cuando los tengas.
