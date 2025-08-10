import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate a unique operation ID for OpenAPI docs.

    Parameters
    ----------
    route : APIRoute
        The API route object.

    Returns
    -------
    str
        Unique operation ID string.
    """
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


async def catch_exceptions_middleware(request: Request, call_next):
    """Middleware to catch unhandled exceptions and return a 500 error.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    call_next : Callable
        The next middleware or route handler.

    Returns
    -------
    Response
        The HTTP response.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.middleware("http")(catch_exceptions_middleware)
    app.middleware("https")(catch_exceptions_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
