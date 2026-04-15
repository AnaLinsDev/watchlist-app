import "dotenv/config";
import z from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().min(1),
  NODE_ENV: z.enum(["dev", "prod"]),
  JWT_SECRET: z.string().min(1),
  JWT_EXPIRES_IN: z.enum(["1d", "7d", "30m"]),
});

export const env = envSchema.parse(process.env);
