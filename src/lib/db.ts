import { drizzle } from "drizzle-orm/mysql2";
import mysql from "mysql2/promise";
import * as schema from "@/db/schema";

const connectionString = process.env.DATABASE_URL;

console.log("DATABASE_URL exists:", !!connectionString);

let db: ReturnType<typeof drizzle> | null = null;

if (connectionString && connectionString.trim() !== "") {
  try {
    console.log("Attempting to connect to database...");
    const poolConnection = mysql.createPool(connectionString);
    db = drizzle(poolConnection, { schema, mode: "default" });
    console.log("Database connection successful");
  } catch (error) {
    console.error("Error connecting to database:", error);
    throw error; // Re-throw to see the actual error
  }
} else {
  console.log("DATABASE_URL is not set or empty");
}

export { db };