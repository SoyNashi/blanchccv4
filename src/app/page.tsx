import { Hero } from "@/components/sections/hero";
import { ProjectsWall } from "@/components/sections/projects-wall";
import { EditorialServices } from "@/components/sections/editorial-services";
import { CertificationsMarquee } from "@/components/sections/certifications-marquee";
import { SecondaryProjects } from "@/components/sections/secondary-projects";
import { BlogSlider } from "@/components/sections/blog-slider";
import { Contact } from "@/components/sections/contact";
import projectsData from "@/data/projects.json";
import servicesData from "@/data/services.json";
import certificationsData from "@/data/certifications.json";
import postsData from "@/data/posts.json";

export default async function Home() {
  // Recuperamos todos los datos de los archivos JSON
  const certs = certificationsData.sort((a, b) => a.order - b.order);
  const latestPosts = postsData
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    .slice(0, 2);
  const allProjects = projectsData.sort((a, b) => a.order - b.order);
  const allServices = servicesData.sort((a, b) => a.order - b.order);

  return (
    <div className="flex flex-col">
      <Hero />
      <ProjectsWall projects={allProjects} />
      <EditorialServices services={allServices} />
      <CertificationsMarquee items={certs.map(c => ({ name: c.name, logo: c.logo }))} />
      <SecondaryProjects />
      <BlogSlider posts={latestPosts} />
      <Contact />
    </div>
  );
}