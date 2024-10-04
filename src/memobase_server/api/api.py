import os
import logging
from dotenv import load_dotenv
from memobase_server.utils import LOG

load_dotenv()

LOG.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "%(levelname)s:    %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
LOG.addHandler(console_handler)
# Done setting up env

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from memobase_server.connector import db_health_check, redis_health_check
from memobase_server.models.response import BaseResponse, CODE


app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.get("/healthcheck")
async def healthcheck() -> BaseResponse:
    LOG.info("Healthcheck requested")
    if not db_health_check():
        raise HTTPException(
            status_code=CODE.INTERNAL_SERVER_ERROR.value,
            detail="Database not available",
        )
    if not redis_health_check():
        raise HTTPException(
            status_code=CODE.INTERNAL_SERVER_ERROR.value,
            detail="Redis not available",
        )
    return BaseResponse()


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth_token = request.headers.get("Authorization")
        if not auth_token or not self.is_valid_token(auth_token):
            return JSONResponse(
                status_code=CODE.UNAUTHORIZED.value,
                content=BaseResponse(
                    errno=CODE.UNAUTHORIZED.value,
                    errmsg=f"Unauthorized access to {request.url.path}",
                ).model_dump(),
            )
        response = await call_next(request)
        return response

    def is_valid_token(self, token: str) -> bool:
        if not token.startswith("Bearer "):
            return False
        token = token.split(" ")[1]
        access_token = os.getenv("ACCESS_TOKEN")
        if access_token is None:
            return True
        return token == access_token


app.include_router(router)
app.add_middleware(AuthMiddleware)
