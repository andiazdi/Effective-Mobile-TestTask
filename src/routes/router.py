from fastapi import APIRouter

from src.routes.auth.router import auth_router
from src.routes.role.router import role_router
from src.routes.user.router import user_router

api_router = APIRouter(prefix="/api", tags=["api"])
for router in (user_router, auth_router, role_router):
    api_router.include_router(router)
