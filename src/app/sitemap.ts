import { MetadataRoute } from 'next'
import posts from '@/data/posts.json'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://blanch.cc'
  
  const postUrls = posts
    .filter(post => post.published)
    .map((post) => ({
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: new Date(post.createdAt),
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    }))

  return [
    {
      url: baseUrl,
      lastModified: new Date('2024-01-01'),
      changeFrequency: 'weekly' as const,
      priority: 1,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date('2024-06-12'),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/certifications`,
      lastModified: new Date('2024-01-01'),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    },
    ...postUrls,
  ]
}
