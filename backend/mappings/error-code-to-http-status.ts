import { ErrorCode, HttpStatusCode } from "../src/enums";

const ErrorCodeToHttpStatus: Record<ErrorCode, number> = {
  // Generic
  [ErrorCode.INTERNAL_SERVER_ERROR]: HttpStatusCode.INTERNAL_SERVER_ERROR,
  [ErrorCode.UNKNOWN_ERROR]: HttpStatusCode.INTERNAL_SERVER_ERROR,

  // Validation
  [ErrorCode.VALIDATION_ERROR]: HttpStatusCode.BAD_REQUEST,
  [ErrorCode.INVALID_INPUT]: HttpStatusCode.BAD_REQUEST,
  [ErrorCode.MISSING_FIELDS]: HttpStatusCode.BAD_REQUEST,

  // Auth
  [ErrorCode.UNAUTHORIZED]: HttpStatusCode.UNAUTHORIZED,
  [ErrorCode.FORBIDDEN]: HttpStatusCode.FORBIDDEN,
  [ErrorCode.INVALID_CREDENTIALS]: HttpStatusCode.UNAUTHORIZED,
  [ErrorCode.TOKEN_EXPIRED]: HttpStatusCode.UNAUTHORIZED,
  [ErrorCode.TOKEN_INVALID]: HttpStatusCode.UNAUTHORIZED,

  // User
  [ErrorCode.USER_NOT_FOUND]: HttpStatusCode.NOT_FOUND,
  [ErrorCode.USER_ALREADY_EXISTS]: HttpStatusCode.CONFLICT,

  // Resource
  [ErrorCode.NOT_FOUND]: HttpStatusCode.NOT_FOUND,
  [ErrorCode.RESOURCE_ALREADY_EXISTS]: HttpStatusCode.CONFLICT,

  // Database
  [ErrorCode.DATABASE_ERROR]: HttpStatusCode.INTERNAL_SERVER_ERROR,
  [ErrorCode.UNIQUE_CONSTRAINT_VIOLATION]: HttpStatusCode.CONFLICT,
  [ErrorCode.FOREIGN_KEY_CONSTRAINT]: HttpStatusCode.BAD_REQUEST,

  // Requests
  [ErrorCode.BAD_REQUEST]: HttpStatusCode.BAD_REQUEST,
  [ErrorCode.CONFLICT]: HttpStatusCode.CONFLICT,
  [ErrorCode.TOO_MANY_REQUESTS]: HttpStatusCode.TOO_MANY_REQUESTS,

  // External
  [ErrorCode.EXTERNAL_SERVICE_ERROR]: HttpStatusCode.INTERNAL_SERVER_ERROR,
  [ErrorCode.TIMEOUT]: HttpStatusCode.SERVICE_UNAVAILABLE,
};

export const getHttpStatusFromErrorCode = (code: ErrorCode): number => {
  return ErrorCodeToHttpStatus[code] || HttpStatusCode.INTERNAL_SERVER_ERROR;
};

/*
How to use this mapping:

Example:

import { getHttpStatusFromErrorCode } from "@/mappings/error-code-to-http-status";
import { ErrorCode } from "@/enums";

const statusCode = getHttpStatusFromErrorCode(ErrorCode.NOT_FOUND);

// statusCode === 404

Typical usage (Express):

res.status(getHttpStatusFromErrorCode(err.code)).json({
  code: err.code,
  message: err.message,
});
*/
