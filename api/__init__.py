from fastapi import APIRouter

from core.config import settings
from .api_v1 import router as router_api_v1
from .api_v1.jwt.jwt_auth import router as router_jwt_auth


router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    router_api_v1,
)

router.include_router(router_jwt_auth)