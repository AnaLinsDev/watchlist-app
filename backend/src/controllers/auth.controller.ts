import { Request, Response, NextFunction } from "express";
import { prisma } from "../config/db";
import { ErrorCode, HttpStatusCode } from "../enums";
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

    res.status(HttpStatusCode.CREATED).json({
      status: "success",
      data: {
        user: {
          id: newUser.id,
          name: name,
          email: email,
        },
      },
    });
  } catch (err) {
    next(err);
  }
};

const login = async (
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> => {
  try {
    const { email, password } = req.body;

    const user = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (!user) {
      throw {
        code: ErrorCode.USER_NOT_FOUND,
      };
    }

    //Validate Password
    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      throw {
        code: ErrorCode.INVALID_CREDENTIALS,
      };
    }

    res.status(HttpStatusCode.OK).json({
      status: "success",
      data: {
        user: {
          id: user.id,
          name: name,
          email: email,
        },
      },
    });
  } catch (err) {
    next(err);
  }
};

export { register, login };
