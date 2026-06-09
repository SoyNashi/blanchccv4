import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle', // Carpeta donde se guardarán las migraciones
  dialect: 'mysql',
  dbCredentials: {
    url: process.env.DATABASE_URL!, // Asegúrate de que DATABASE_URL esté definida
  },
});