from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.errors import AppError
from app.core.errors import ErrorCode
from app.core.error_map import ERROR_MAP

async def app_error_handler(request: Request, exc: AppError):
    error = ERROR_MAP.get(exc.code)

    if not error:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "UNKNOWN_ERROR",
                    "message": "Unknown error"
                }
            }
        )

    return JSONResponse(
        status_code=error["status"],
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": error["message"]
            }
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal Server Error"
            }
        }
    )