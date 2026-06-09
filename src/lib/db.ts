import { drizzle } from "drizzle-orm/mysql2";
import mysql from "mysql2/promise";
import * as schema from "../db/schema";

const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  throw new Error("DATABASE_URL no está definida en las variables de entorno");
}

// Creamos un pool de conexiones para reutilizar en el Edge
const poolConnection = mysql.createPool(connectionString);
export const db = drizzle(poolConnection, { schema, mode: "default" });