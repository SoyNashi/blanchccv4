import { MetadataRoute } from 'next'
import posts from '@/data/posts.json'

export async function GET() {
  const baseUrl = 'https://blanch.cc'
  
  const publishedPosts = posts
    .filter(post => post.published !== false)
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())

  const rssItems = publishedPosts.map(post => {
    const keywords = post.keywords || []
    const keywordTags = keywords.map(kw => `<category>${kw}</category>`).join('')
    
    return `
    <item>
      <title><![CDATA[${post.title}]]></title>
      <link>${baseUrl}/blog/${post.slug}</link>
      <description><![CDATA[${post.description}]]></description>
      <category>${post.category}</category>
      <pubDate>${new Date(post.createdAt).toUTCString()}</pubDate>
      <guid isPermaLink="false">${post.id}</guid>
      ${keywordTags}
    </item>`
  }).join('')

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Nil Blanch - Blog</title>
    <link>${baseUrl}/blog</link>
    <description><![CDATA[Artículos sobre desarrollo web, seguridad, arquitectura de sistemas y tecnología]]></description>
    <language>es</language>
    <atom:link href="${baseUrl}/rss.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    ${rssItems}
  </channel>
</rss>`

  return new Response(rss, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  })
}
