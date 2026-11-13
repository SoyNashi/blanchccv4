import legacyPosts from "./posts.json";
import secondArchive from "./posts-02.json";

// Cada archivo de archivo debe contener como máximo 50 artículos.
// Para añadir uno nuevo: crea posts-03.json, impórtalo aquí y añádelo a archiveFiles.
// Esta separación permite migrar los archivos a una fuente externa en el futuro
// sin cambiar los componentes que consumen la colección unificada.
export const MAX_POSTS_PER_FILE = 50;

const archiveFiles = [
  { name: "posts.json", posts: legacyPosts },
  { name: "posts-02.json", posts: secondArchive },
] as const;

for (const archive of archiveFiles) {
  if (archive.posts.length > MAX_POSTS_PER_FILE) {
    throw new Error(
      `El archivo ${archive.name} supera el máximo de ${MAX_POSTS_PER_FILE} artículos.`
    );
  }
}

const allPosts = archiveFiles.flatMap((archive) => archive.posts);
const slugs = new Set<string>();
const ids = new Set<string>();

for (const post of allPosts) {
  if (slugs.has(post.slug)) {
    throw new Error(`Slug de artículo duplicado: ${post.slug}`);
  }
  if (ids.has(post.id)) {
    throw new Error(`ID de artículo duplicado: ${post.id}`);
  }
  slugs.add(post.slug);
  ids.add(post.id);
}

export default allPosts;
