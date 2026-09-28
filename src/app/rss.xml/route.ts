import { remark } from 'remark'
import remarkGfm from 'remark-gfm'
import remarkHtml from 'remark-html'
import posts from '@/data/posts.json'
import projects from '@/data/projects.json'
import secondaryProjects from '@/data/secondary-projects.json'

const BASE_URL = 'https://blanch.cc'
const PLACEHOLDER_BASE = 'https://placehold.co/1200x630/111111/FFFFFF/png'

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

function placeholderImage(title: string) {
  return `${PLACEHOLDER_BASE}?text=${encodeURIComponent(`BLANCH.CC · ${title}`)}`
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
  const image = placeholderImage(post.title)
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
      <media:content url="${escapeXml(image)}" type="image/png" medium="image" width="1200" height="630" />
      <media:thumbnail url="${escapeXml(image)}" width="1200" height="630" />
      <media:title>${cdata(post.title)}</media:title>
    </item>`
}

type Project = {
  id?: string
  title?: string
  name?: string
  description?: string
  details?: string
  link?: string
  image?: string
  tags?: string[]
  tech?: string[] | { label?: string; value?: string }[]
}

function flattenSecondaryProjects() {
  return Object.entries(secondaryProjects).flatMap(([category, items]) =>
    items.map((item) => ({ ...item, category }))
  )
}

async function projectToRssItem(project: Project, category = 'Proyecto') {
  const title = project.title || project.name || 'Proyecto'
  const description = project.description || project.details || ''
  const details = project.details && project.details !== description ? project.details : ''
  const image = placeholderImage(title)
  const tags = [
    category,
    ...(project.tags || []),
    ...(project.tech || []).map((tech) =>
      typeof tech === 'string' ? tech : tech.label || tech.value || ''
    ),
  ].filter(Boolean)
  const projectUrl =
    project.link ||
    `${BASE_URL}/#${encodeURIComponent(title.toLowerCase().replace(/\s+/g, '-'))}`
  const projectHtml = `
    <figure>
      <img src="${escapeXml(image)}" alt="${escapeXml(title)}" width="1200" height="630" />
      <figcaption>${escapeXml(title)}</figcaption>
    </figure>
    <h2>${escapeXml(title)}</h2>
    <p>${escapeXml(description)}</p>
    ${details ? `<h3>Detalles</h3><p>${escapeXml(details)}</p>` : ''}
    ${tags.length ? `<p><strong>Tags:</strong> ${tags.map((tag) => `#${escapeXml(tag)}`).join(' ')}</p>` : ''}
    <p><a href="${escapeXml(projectUrl)}">Ver proyecto</a></p>
  `
  const categories = tags
    .map((tag) => `<category>${cdata(String(tag))}</category>`)
    .join('\n      ')
  const guid = `${BASE_URL}/rss/projects/${encodeURIComponent(
    String(project.id || title).toLowerCase().replace(/[^a-z0-9]+/g, '-')
  )}`

  return `
    <item>
      <title>${cdata(title)}</title>
      <link>${escapeXml(projectUrl)}</link>
      <description>${cdata(projectHtml)}</description>
      <content:encoded>${cdata(projectHtml)}</content:encoded>
      ${categories}
      <dc:creator>Nil Blanch</dc:creator>
      <guid isPermaLink="false">${escapeXml(guid)}</guid>
      <media:content url="${escapeXml(image)}" type="image/png" medium="image" width="1200" height="630" />
      <media:thumbnail url="${escapeXml(image)}" width="1200" height="630" />
      <media:title>${cdata(title)}</media:title>
    </item>`
}

export async function GET() {
  const publishedPosts = posts
    .filter((post) => post.published !== false)
    .sort(
      (a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )

  const primaryProjects = projects.map((project) => ({
    ...project,
    category: 'Proyecto principal',
  }))
  const allProjects = [...primaryProjects, ...flattenSecondaryProjects()]

  const postItems = await Promise.all(publishedPosts.map(postToRssItem))
  const projectItems = await Promise.all(
    allProjects.map((project) => projectToRssItem(project, project.category))
  )

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
${projectItems.join('\n')}
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
