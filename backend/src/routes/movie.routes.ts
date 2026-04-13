import express from "express";

const router = express.Router();

// Get data from the TMDb
router.get("/", (req, res) => {
  res.json({ message: "GET" });
});

export default router;
