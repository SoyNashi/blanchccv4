import { remark } from 'remark'
import remarkGfm from 'remark-gfm'
import remarkHtml from 'remark-html'
import posts from '@/data/posts.json'

const BASE_URL = 'https://blanch.cc'
const DEFAULT_FEED_IMAGE = 'https://raw.githubusercontent.com/SoyNashi/blanchccv4/main/src/app/rss.xml/6Rd61.jpg'

function escapeXml(value: unknown) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

function cdata(value: string) {
  return `<![CDATA[${value.replace(/\]\]>/g, ']]]]><![CDATA[>')}]]>`
}

function feedImage(path?: string) {
  if (!path) return DEFAULT_FEED_IMAGE
  if (/^https?:\/\//i.test(path)) return path
  return `${BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
}

async function markdownToHtml(markdown: string) {
  const result = await remark().use(remarkGfm).use(remarkHtml).process(markdown)
  return String(result)
}

function metadataHtml(post: (typeof posts)[number]) {
  const tags = post.keywords?.length
    ? `<ul>${post.keywords.map((keyword) => `<li>#${escapeXml(keyword)}</li>`).join('')}</ul>`
    : ''

  return `
    <aside>
      <p><strong>Categoría:</strong> ${escapeXml(post.category)}</p>
      <p><strong>Fecha:</strong> ${escapeXml(new Date(post.createdAt).toISOString())}</p>
      <p><strong>Lectura:</strong> ${escapeXml(post.readingTime)} min</p>
      <p><strong>Palabras:</strong> ${escapeXml(post.wordCount)}</p>
      ${post.featured ? '<p><strong>Destacado:</strong> sí</p>' : ''}
      ${post.series ? `<p><strong>Serie:</strong> ${escapeXml(post.series)}</p>` : ''}
      ${tags ? '<p><strong>Tags:</strong></p>' + tags : ''}
    </aside>
  `
}

async function postToRssItem(post: (typeof posts)[number]) {
  const image = DEFAULT_FEED_IMAGE
  const articleHtml = await markdownToHtml(post.content)
  const fullContent = `
    <figure>
      <img src="${escapeXml(image)}" alt="${escapeXml(post.title)}" width="1200" height="630" />
      <figcaption>${escapeXml(post.title)}</figcaption>
    </figure>
    <p>${escapeXml(post.description)}</p>
    ${metadataHtml(post)}
    <hr />
    ${articleHtml}
  `
  const categories = [post.category, ...(post.keywords || [])]
    .filter(Boolean)
    .map((tag) => `<category>${cdata(String(tag))}</category>`)
    .join('\n      ')

  return `
    <item>
      <title>${cdata(post.title)}</title>
      <link>${BASE_URL}/blog/${encodeURIComponent(post.slug)}</link>
      <description>${cdata(fullContent)}</description>
      <content:encoded>${cdata(fullContent)}</content:encoded>
      ${categories}
      <pubDate>${new Date(post.createdAt).toUTCString()}</pubDate>
      <dc:creator>Nil Blanch</dc:creator>
      <guid isPermaLink="true">${BASE_URL}/blog/${encodeURIComponent(post.slug)}</guid>
      <enclosure url="${escapeXml(image)}" type="${image === DEFAULT_FEED_IMAGE ? 'image/jpeg' : 'image/png'}" length="0" />
      <media:content url="${escapeXml(image)}" type="${image === DEFAULT_FEED_IMAGE ? 'image/jpeg' : 'image/png'}" medium="image" width="1200" height="630" />
      <media:thumbnail url="${escapeXml(image)}" width="1200" height="630" />
      <media:title>${cdata(post.title)}</media:title>
    </item>`
}

export async function GET() {
  const publishedPosts = posts
    .filter((post) => post.published !== false)
    .sort(
      (a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )

  const postItems = await Promise.all(publishedPosts.map(postToRssItem))

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Nil Blanch - Blanch.cc</title>
    <link>${BASE_URL}</link>
    <description>${cdata(
      'Publicaciones y proyectos de Nil Blanch: desarrollo web, programación, IA, tecnología y experimentos.'
    )}</description>
    <language>es</language>
    <atom:link href="${BASE_URL}/rss.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <generator>Next.js RSS</generator>
${postItems.join('\n')}
  </channel>
</rss>`

  return new Response(rss, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
      'X-Content-Type-Options': 'nosniff',
    },
  })
}
