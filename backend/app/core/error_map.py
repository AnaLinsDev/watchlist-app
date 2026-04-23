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
    ErrorCode.NOT_AUTHENTICATED: {
        "status": 401,
        "message": "Not authenticated",
    },
    ErrorCode.INVALID_TOKEN: {
        "status": 401,
        "message": "Invalid token",
    },

    # DEFAULT
    ErrorCode.NOT_FOUND: {
        "status": 404,
        "message": "Resource not found",
    },
}
