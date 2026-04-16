from app.core.errors import ErrorCode


ERROR_MAP = {
    # AUTH
    ErrorCode.USER_ALREADY_EXISTS: {
        "status": 400,
        "message": "Email or username already exists",
    },
    ErrorCode.INVALID_CREDENTIALS: {
        "status": 401,
        "message": "Invalid credentials",
    },
    ErrorCode.USER_NOT_FOUND: {
        "status": 404,
        "message": "User not found",
    },

    # DEFAULT
    ErrorCode.NOT_FOUND: {
        "status": 404,
        "message": "Resource not found",
    },
}
