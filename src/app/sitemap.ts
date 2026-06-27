import { MetadataRoute } from 'next'
import posts from '@/data/posts.json'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://blanch.cc'
  
  const postUrls = posts
    .filter(post => post.published)
    .map((post) => {
      let lastModified = new Date()
      try {
        if (post.createdAt) {
          const parsedDate = new Date(post.createdAt)
          if (!isNaN(parsedDate.getTime())) {
            lastModified = parsedDate
          }
        }
      } catch (e) {
        console.error('Invalid date for post:', post.slug, post.createdAt)
      }
      
      return {
        url: `${baseUrl}/blog/${post.slug}`,
        lastModified,
        changeFrequency: 'monthly' as const,
        priority: 0.6,
      }
    })

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
