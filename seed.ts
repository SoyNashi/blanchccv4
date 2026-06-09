import { db } from "@/lib/db";
import { services, projects, certifications, postsMeta } from "./schema";
import { v4 as uuidv4 } from "uuid";

async function seed() {
  console.log("🌱 Iniciando carga de datos...");

  // Limpiar tablas (Opcional, cuidado en producción)
  // await db.delete(services);

  await db.insert(services).values([
    { id: uuidv4(), title: "Desarrollo Web", description: "Aplicaciones web de alto rendimiento...", order: 1 },
    { id: uuidv4(), title: "Ecommerce", description: "Soluciones de comercio electrónico...", order: 2 },
    { id: uuidv4(), title: "SEO Técnico", description: "Optimización profunda desde el código...", order: 3 },
    { id: uuidv4(), title: "Hosting & Ops", description: "Infraestructura gestionada...", order: 4 },
    { id: uuidv4(), title: "Mantenimiento", description: "Cuidado constante y evolución...", order: 5 },
    { id: uuidv4(), title: "Consultoría", description: "Asesoramiento estratégico...", order: 6 },
  ]);

  await db.insert(projects).values([
    {
      id: uuidv4(),
      title: "Blau360",
      description: "Digitalización a medida para PYMES...",
      image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
      tags: ["Product Strategy", "Full Stack Dev"],
      tech: [{ label: "Frontend", value: "Next.js" }, { label: "Backend", value: "PostgreSQL" }],
      color: "#0055ff",
      order: 1
    },
    {
      id: uuidv4(),
      title: "Bastet Project",
      description: "Marca de ropa impulsada por valores...",
      image: "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800",
      tags: ["E-commerce", "UX Design"],
      tech: [{ label: "Storefront", value: "Shopify" }, { label: "Automation", value: "Klaviyo" }],
      color: "#ff3300",
      order: 2
    }
  ]);

  await db.insert(certifications).values([
    { id: uuidv4(), name: "AWS Certified", logo: "https://upload.wikimedia.org/wikipedia/commons/5/5c/AWS_Simple_Icons_AWS_Cloud.svg", order: 1 },
    { id: uuidv4(), name: "Google Cloud", logo: "https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg", order: 2 },
    { id: uuidv4(), name: "Meta Frontend", logo: "https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg", order: 3 },
    // Añade más aquí...
  ]);

  // Sincronizar posts del JSON a la DB
  await db.insert(postsMeta).values([
    { id: uuidv4(), slug: "optimizacion-nextjs-seo", likes: 124 },
    { id: uuidv4(), slug: "alerta-malware-npm", likes: 45 }
  ]).onDuplicateKeyUpdate({ set: { likes: 124 } });

  console.log("✅ Datos cargados correctamente.");
  process.exit(0);
}

seed().catch((e) => {
  console.error("❌ Error en el seed:", e);
  process.exit(1);
});