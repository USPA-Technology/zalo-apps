from fastapi import APIRouter
# from .routers.kiotviet import router as kioviet_router
from .routers.zalo import router as zalo_router
from .routers.kiotviet.router import router as kioviet_webhook


router = APIRouter(prefix="/v1")
router.include_router(zalo_router)
router.include_router(kioviet_webhook)