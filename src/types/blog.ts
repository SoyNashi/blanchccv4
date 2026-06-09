export type PostCategory = 'novedad' | 'alerta' | 'descubrimiento' | 'creacion' | 'seguridad' | 'malware';

export interface Post {
  id: string;
  slug: string;
  title: string;
  description: string;
  content: string; // Markdown
  category: PostCategory;
  publishedAt: string;
  likes: number;
}
