from fastapi import APIRouter
# from .routers.kiotviet import router as kioviet_router
from .routers.zalo import router as zalo_router

from .routers.kiotviet.router import router as kiotvet
from .routers.demo.main import router as demo

router = APIRouter(prefix="/v1")

router.include_router(zalo_router)
router.include_router(kiotvet)
router.include_router(demo)