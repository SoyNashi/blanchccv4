import { drizzle } from "drizzle-orm/mysql2";
import mysql from "mysql2/promise";
import * as schema from "@/db/schema";

const connectionString = process.env.DATABASE_URL;

let db: ReturnType<typeof drizzle> | null = null;

if (connectionString && connectionString.trim() !== "") {
  try {
    const poolConnection = mysql.createPool(connectionString);
    db = drizzle(poolConnection, { schema, mode: "default" });
  } catch (error) {
    console.error("Error connecting to database:", error);
  }
}

export { db };