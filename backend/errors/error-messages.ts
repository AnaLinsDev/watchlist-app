import { ErrorCode } from "../src/enums/error-code";

export const ErrorMessages: Partial<Record<ErrorCode, string>> = {
  // Auth
  [ErrorCode.USER_NOT_FOUND]: "User not found",
  [ErrorCode.USER_ALREADY_EXISTS]: "User already exists",
  [ErrorCode.UNAUTHORIZED]: "Unauthorized",
  [ErrorCode.FORBIDDEN]: "Forbidden",
  [ErrorCode.INVALID_CREDENTIALS]: "Invalid Credentials",

  // Validation
  [ErrorCode.VALIDATION_ERROR]: "Invalid request data",

  // Default
  [ErrorCode.INTERNAL_SERVER_ERROR]: "Something went wrong",
  [ErrorCode.UNKNOWN_ERROR]: "Something went wrong",
};

export const getDefaultMessage = (code: ErrorCode): string => {
  return ErrorMessages[code] || "Something went wrong";
};
