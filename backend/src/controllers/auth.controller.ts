import { Request, Response, NextFunction } from "express";
import { loginUser, registerUser } from "../services/auth.service";
import { generateToken } from "../helper/generate-token";
import { HttpStatusCode } from "../enums";

const register = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { name, email, password } = req.body;

    const user = await registerUser(name, email, password);

    generateToken(user.id, res);

    res.status(HttpStatusCode.CREATED).json({
      status: "success",
      data: {
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
        },
      },
    });
  } catch (err) {
    next(err);
  }
};

const login = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { email, password } = req.body;

    const user = await loginUser(email, password);

    generateToken(user.id, res);

    res.status(HttpStatusCode.OK).json({
      status: "success",
      data: {
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
        },
      },
    });
  } catch (err) {
    next(err);
  }
};

const logout = async (req: Request, res: Response) => {
  res.cookie("jwt", "", {
    httpOnly: true,
    expires: new Date(0),
  });

  res.status(HttpStatusCode.OK).json({
    status: "success",
    message: "Logged out successfully",
  });
};

export { register, login, logout };
