import express from "express";
import "dotenv/config";

// Routes
import movieRoutes from "./routes/movie.routes";
import healthRoutes from "./routes/health.routes";
import { connectDB, disconnectDB } from "./config/db";

const app = express();
const PORT = 5001;

app.use(express.json());

// API Routes
app.use("/movies", movieRoutes);
app.use("/health", healthRoutes);

let server: any;

const startServer = async () => {
  try {
    await connectDB();

    server = app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
};

const shutdown = async (code = 1) => {
  try {
    if (server) {
      await new Promise((resolve) => server.close(resolve));
    }
    await disconnectDB();
  } finally {
    process.exit(code);
  }
};

// Process handlers
process.on("unhandledRejection", (err) => {
  console.error("Unhandled Rejection:", err);
  shutdown(1);
});

process.on("uncaughtException", (err) => {
  console.error("Uncaught Exception:", err);
  shutdown(1);
});

process.on("SIGTERM", () => {
  console.log("SIGTERM received, shutting down gracefully");
  shutdown(0);
});

// Start app
startServer();
