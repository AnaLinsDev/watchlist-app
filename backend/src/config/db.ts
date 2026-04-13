import { PrismaClient } from "@prisma/client";
import { env } from "../../env";

const prisma = new PrismaClient({
  log: env.NODE_ENV == "dev" ? ["query", "error", "warn"] : ["error"],
});

const connectDB = async () => {
  try {
    await prisma.$connect();
    console.log("DB Connected via Prisma");
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.log(`Database connection error: ${error.message}`);
    } else {
      console.log("Unknown database error");
    }
    process.exit(1);
  }
};

const disconnectDB = async () => {
  await prisma.$disconnect();
};

export { prisma, connectDB, disconnectDB };
