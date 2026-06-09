import { Hero } from "@/components/sections/hero";
import { ProjectsWall } from "@/components/sections/projects-wall";
import { EditorialServices } from "@/components/sections/editorial-services";
import { Certifications } from "@/components/sections/certifications";
import { SecondaryProjects } from "@/components/sections/secondary-projects";
import { BlogSlider } from "@/components/sections/blog-slider";
import { Contact } from "@/components/sections/contact";

export default function Home() {
  return (
    <div className="flex flex-col">
      <Hero />
      <ProjectsWall />
      <EditorialServices />
      <Certifications />
      <SecondaryProjects />
      <BlogSlider />
      <Contact />
    </div>
  );
}
