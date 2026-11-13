import ReferenceHome from "@/components/sections/reference-home";
import projectsData from "@/data/projects.json";
import servicesData from "@/data/services.json";
import certificationsData from "@/data/certifications.json";
import secondaryProjects from "@/data/secondary-projects.json";
import postsData from "@/data/posts";
export default function Home(){
 return <ReferenceHome projects={[...projectsData].sort((a,b)=>a.order-b.order)} services={[...servicesData].sort((a,b)=>a.order-b.order)} certifications={[...certificationsData].sort((a,b)=>a.order-b.order)} secondaryProjects={secondaryProjects} posts={[...postsData].sort((a,b)=>new Date(b.createdAt).getTime()-new Date(a.createdAt).getTime())}/>;
}
