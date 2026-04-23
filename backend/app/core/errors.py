from enum import Enum


class ErrorCode(str, Enum):
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    NOT_FOUND = "NOT_FOUND"


class AppError(Exception):
    def __init__(self, code: ErrorCode):
        self.code = code
