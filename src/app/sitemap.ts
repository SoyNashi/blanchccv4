import { MetadataRoute } from 'next'
import posts from '@/data/posts.json'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://blanch.cc'

  // Generar URLs dinámicamente desde los posts
  const postUrls = posts
    .filter(post => post.published !== false)
    .map(post => ({
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: post.createdAt ? new Date(post.createdAt) : new Date('2024-01-01'),
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    }))

  return [
    {
      url: baseUrl,
      lastModified: new Date('2024-01-01'),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date('2024-01-01'),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    ...postUrls,
    {
      url: `${baseUrl}/certifications`,
      lastModified: new Date('2024-01-01'),
      changeFrequency: 'monthly',
      priority: 0.7,
    },
  ]
}
