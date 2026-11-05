import Link from "next/link";
import posts from "@/data/posts.json";
import {notFound} from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ReferenceNav from "@/components/reference-nav";
import ReferenceFooter from "@/components/reference-footer";
import CopyArticleLink from "@/components/blog/copy-article-link";
import ReferenceToc from "@/components/blog/reference-toc";
function slugify(s:string){return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9\s-]/g,"").trim().replace(/\s+/g,"-").replace(/-+/g,"-")}
function plain(children:React.ReactNode):string{return Array.isArray(children)?children.map(plain).join(""):typeof children==="string"||typeof children==="number"?String(children):null!==children&&typeof children==="object"&&"props" in children?plain((children as React.ReactElement<any>).props.children):""}
function extractHeadings(markdown:string){return Array.from(markdown.matchAll(/^#{1,3}\s+(.+)$/gm)).map(m=>({text:m[1].trim(),id:slugify(m[1].trim()),level:m[0].match(/^#+/)?.[0].length||1}))}
type PageProps={params:Promise<{slug:string}>};
export const dynamic="force-static";
export async function generateStaticParams(){return posts.filter(p=>p.published).map(p=>({slug:p.slug}))}
export async function generateMetadata({params}:PageProps){const {slug}=await params;const post=posts.find(p=>p.slug===slug&&p.published);return post?{title:post.title,description:post.description,alternates:{canonical:`https://blanch.cc/blog/${slug}`},openGraph:{title:post.title,description:post.description,type:"article",publishedTime:post.createdAt}}:{title:"Artículo no encontrado"}}
export default async function BlogPostPage({params}:PageProps){
 const {slug}=await params;const post=posts.find(p=>p.slug===slug&&p.published);if(!post)notFound();
 const all=posts.filter(p=>p.published).sort((a,b)=>new Date(b.createdAt).getTime()-new Date(a.createdAt).getTime());
 const series=post.series?all.filter(p=>p.series===post.series).sort((a,b)=>(a.seriesOrder||0)-(b.seriesOrder||0)):[],seriesIndex=series.findIndex(p=>p.slug===slug),prev=seriesIndex>0?series[seriesIndex-1]:null,nextSeries=seriesIndex>=0?series[seriesIndex+1]:null;
 const position=all.findIndex(p=>p.slug===slug),next=all[position+1]||all[0],headings=extractHeadings(post.content);
 return <div data-view="post"><ReferenceNav/><section className="pk"><Link href="/blog" className="back">← VOLVER AL BLOG</Link><div className="meta mono"><span className="stamp">{post.category}</span><span>{new Date(post.createdAt).toLocaleDateString("es-ES",{day:"numeric",month:"long",year:"numeric"})}</span><span>{post.readingTime||1} MIN DE LECTURA</span></div><h1 className="disp">{post.title}</h1><p className="lede">{post.description}</p></section>
 <section className="ref-article-layout"><ReferenceToc headings={headings}/><article className="ref-prose"><ReactMarkdown remarkPlugins={[remarkGfm]} components={{h1:({children})=><h2 id={slugify(plain(children))}>{children}</h2>,h2:({children})=><h2 id={slugify(plain(children))}>{children}</h2>,h3:({children})=><h3 id={slugify(plain(children))}>{children}</h3>,h4:({children})=><h4 id={slugify(plain(children))}>{children}</h4>,img:({src,alt})=><img src={src||""} alt={alt||""}/>,a:({href,children})=><a href={href} target={href?.startsWith("http")?"_blank":undefined} rel={href?.startsWith("http")?"noreferrer":undefined}>{children}</a>}}>{post.content}</ReactMarkdown><div className="by"><div className="av">NB</div><p><b>NIL BLANCH</b><br/>Desarrollador de aplicaciones y web</p><CopyArticleLink/></div></article><aside className="ref-article-info"><section><h3>INFORMACIÓN</h3><p>{post.readingTime||1} MIN DE LECTURA</p><p>{post.wordCount||0} PALABRAS</p><p>{new Date(post.createdAt).toLocaleDateString("es-ES")}</p>{post.featured&&<b>DESTACADO</b>}</section><section><h3>PALABRAS CLAVE</h3><div>{(post.keywords||[]).map(k=><span key={k}>#{k}</span>)}</div></section></aside></section>
 {series.length>1&&<section className="ref-series"><span>SERIE / {post.series} — PARTE {seriesIndex+1} DE {series.length}</span><div>{prev&&<Link href={`/blog/${prev.slug}`}>← ANTERIOR</Link>}{series.map((p,i)=><Link key={p.id} href={`/blog/${p.slug}`} aria-current={p.slug===slug?"page":undefined}>{String(i+1).padStart(2,"0")}</Link>)}{nextSeries&&<Link href={`/blog/${nextSeries.slug}`}>SIGUIENTE →</Link>}</div></section>}
 {next&&<Link href={`/blog/${next.slug}`} className="nx"><span className="mono">SIGUIENTE ARTÍCULO ↗</span><h2 className="disp">{next.title}</h2></Link>}
 <section className="ref-about"><span className="mono">SOBRE QUIEN ESCRIBE</span><h2 className="disp">Nil Blanch</h2><p>Desarrollo páginas web y aplicaciones a medida. Me interesa el diseño brutalista, el software propio y que cada persona pueda entender y controlar las herramientas que utiliza.</p><Link href="/#contacto">HABLEMOS ↗</Link></section><ReferenceFooter/></div>;
}
