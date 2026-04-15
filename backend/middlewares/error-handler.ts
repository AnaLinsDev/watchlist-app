import { Request, Response, NextFunction } from "express";
import { ErrorCode } from "../src/enums";
import { getHttpStatusFromErrorCode } from "../mappings/error-code-to-http-status";
import { getDefaultMessage } from "../errors/error-messages";

type AppErrorType = {
  code?: ErrorCode;
  message?: string;
  statusCode?: number;
};

export const errorHandler = (
  err: AppErrorType,
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  const errorCode = err.code || ErrorCode.INTERNAL_SERVER_ERROR;

  const statusCode = err.statusCode || getHttpStatusFromErrorCode(errorCode);

  const message = err.message || getDefaultMessage(errorCode);

  res.status(statusCode).json({
    code: errorCode,
    message,
  });
};
