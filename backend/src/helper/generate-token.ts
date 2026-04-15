import jwt from "jsonwebtoken";
import { env } from "../../env";
import { Response } from "express";
import { getCookieMaxAge } from "../../utils/cookie-time";

export const generateToken = (userId: string, res: Response) => {
  const payload = { id: userId };

  const token = jwt.sign(payload, env.JWT_SECRET as string, {
    expiresIn: env.JWT_EXPIRES_IN,
  });

  res.cookie("jwt", token, {
    httpOnly: true, // Prevents JS access (XSS protection)
    secure: env.NODE_ENV == "prod", // Only HTTPS
    sameSite: "lax", //allows cookies to be sent on normal navigation and same-site requests, but blocks most cross-site requests.
    maxAge: getCookieMaxAge(env.JWT_EXPIRES_IN), // Calculates the time the cookie should live
  });
};
