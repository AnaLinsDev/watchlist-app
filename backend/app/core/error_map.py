from app.core.errors import ErrorCode


ERROR_MAP = {
    # AUTH
    ErrorCode.INVALID_CREDENTIALS: {
        "status": 401,
        "message": "Invalid credentials",
    },
    ErrorCode.NOT_AUTHENTICATED: {
        "status": 401,
        "message": "Not authenticated",
    },
    ErrorCode.INVALID_TOKEN: {
        "status": 401,
        "message": "Invalid token",
    },
    ErrorCode.INVALID_CURRENT_PASSWORD: {
        "status": 400,
        "message": "Invalid current password field",
    },


    # USER
    ErrorCode.USER_NOT_FOUND: {
        "status": 404,
        "message": "User not found",
    },
    ErrorCode.USER_ALREADY_EXISTS: {
        "status": 409,
        "message": "User with the email or username already exists",
    },
    ErrorCode.EMAIL_ALREADY_EXISTS: {
        "status": 409,
        "message": "Email already being used",
    },
    ErrorCode.USERNAME_ALREADY_EXISTS: {
        "status": 409,
        "message": "Username already being used",
    },

    # WATCHLIST
    ErrorCode.MAX_WATCHLISTS_REACHED: {
        "status": 400,
        "message": "Maximum quantity of watchlists reached",
    },
    ErrorCode.WATCHLIST_NAME_EXISTS: {
        "status": 409,
        "message": "Watchlist with the same name already exists",
    },
    ErrorCode.WATCHLIST_NOT_FOUND: {
        "status": 404,
        "message": "Watchlist not found",
    },

    # WATCHLIST ITEMS
    ErrorCode.ITEM_NOT_FOUND: {
        "status": 404,
        "message": "Watchlist item not found",
    },
    ErrorCode.MAX_ITEMS_REACHED: {
        "status": 400,
        "message": "Maximum quantity of items reached",
    },
    ErrorCode.ITEM_ALREADY_EXISTS: {
        "status": 409,
        "message": "Item already exists in the watchlist",
    },

    # DEFAULT
    ErrorCode.NOT_FOUND: {
        "status": 404,
        "message": "Resource not found",
    },
    ErrorCode.FORBIDDEN: {
        "status": 403,
        "message": "Username already being used",
    },
}
