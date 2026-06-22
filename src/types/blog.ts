export type PostCategory = 'novedad' | 'alerta' | 'descubrimiento' | 'creacion' | 'seguridad' | 'malware';

export interface Post {
  id: string;
  slug: string;
  title: string;
  description: string;
  content: string; // Markdown
  category: PostCategory;
  createdAt: string;
  keywords: string[];
  readingTime: number;
  wordCount: number;
  featured: boolean;
  published: boolean;
  series: string | null;
  seriesOrder: number | null;
  seriesPartTitle: string | null;
}
