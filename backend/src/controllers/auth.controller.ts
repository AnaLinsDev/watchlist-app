import { Request, Response, NextFunction } from "express";
import { prisma } from "../config/db";
import { ErrorCode } from "../enums";
import bcrypt from "bcryptjs";

const register = async (
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> => {
  try {
    const { name, email, password } = req.body;

    const user = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (user) {
      throw {
        code: ErrorCode.USER_ALREADY_EXISTS,
      };
    }

    //Hash Password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const newUser = await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
      },
    });

    res.status(201).json(newUser);
  } catch (err) {
    next(err);
  }
};

export { register };
