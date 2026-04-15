import bcrypt from "bcryptjs";
import { prisma } from "../config/db";
import { ErrorCode } from "../enums";

export const registerUser = async (
  name: string,
  email: string,
  password: string,
) => {
  const existingUser = await prisma.user.findUnique({ where: { email } });

  if (existingUser) {
    throw { code: ErrorCode.USER_ALREADY_EXISTS };
  }

  const hashedPassword = await bcrypt.hash(password, 10);

  const user = await prisma.user.create({
    data: { name, email, password: hashedPassword },
  });

  return user;
};

export const loginUser = async (email: string, password: string) => {
  const user = await prisma.user.findUnique({ where: { email } });

  if (!user) {
    throw { code: ErrorCode.USER_NOT_FOUND };
  }

  const isValid = await bcrypt.compare(password, user.password);

  if (!isValid) {
    throw { code: ErrorCode.INVALID_CREDENTIALS };
  }

  return user;
};
