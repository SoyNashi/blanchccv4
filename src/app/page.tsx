import { Hero } from "@/components/sections/hero";
import { ProjectsWall } from "@/components/sections/projects-wall";
import { EditorialServices } from "@/components/sections/editorial-services";
import { CertificationsMarquee } from "@/components/sections/certifications-marquee";
import { SecondaryProjects } from "@/components/sections/secondary-projects";
import { BlogSlider } from "@/components/sections/blog-slider";
import { Contact } from "@/components/sections/contact";
import { db } from "@/lib/db";
import { certifications, postsMeta, projects, services } from "@/db/schema";
import { desc } from "drizzle-orm";

export default async function Home() {
  // Recuperamos todos los datos en paralelo para máxima velocidad
  const [certs, latestPosts, allProjects, allServices] = await Promise.all([
    db.select().from(certifications).orderBy(certifications.order),
    db.select().from(postsMeta).orderBy(desc(postsMeta.createdAt)).limit(2),
    db.select().from(projects).orderBy(projects.order),
    db.select().from(services).orderBy(services.order),
  ]).catch(() => [[], [], [], []]);

  return (
    <div className="flex flex-col">
      <Hero />
      <ProjectsWall projects={allProjects} />
      <EditorialServices services={allServices} />
      <CertificationsMarquee items={certs.map(c => ({ name: c.name, logo: c.logo_url }))} />
      <SecondaryProjects />
      <BlogSlider posts={latestPosts} />
      <Contact />
    </div>
  );
}