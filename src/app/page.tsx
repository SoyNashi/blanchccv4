import { Hero } from "@/components/sections/hero";
import { ProjectsWall } from "@/components/sections/projects-wall";
import { EditorialServices } from "@/components/sections/editorial-services";
import { CertificationsMarquee } from "@/components/sections/certifications-marquee";
import { SecondaryProjects } from "@/components/sections/secondary-projects";
import { BlogSlider } from "@/components/sections/blog-slider";
import { Contact } from "@/components/sections/contact";
import { db } from "@/lib/db";
import { certifications, postsMeta } from "@/db/schema";
import { desc } from "drizzle-orm";

export default async function Home() {
  // Fetching real data from DB
  const certs = await db.select().from(certifications).orderBy(certifications.order).catch(() => []);
  const latestPosts = await db.select().from(postsMeta).orderBy(desc(postsMeta.createdAt)).limit(2).catch(() => []);

  return (
    <div className="flex flex-col">
      <Hero />
      <ProjectsWall />
      <EditorialServices />
      <CertificationsMarquee items={certs.map(c => ({ name: c.name, logo: c.logo }))} />
      <SecondaryProjects />
      <BlogSlider posts={latestPosts} />
      <Contact />
    </div>
  );
}
