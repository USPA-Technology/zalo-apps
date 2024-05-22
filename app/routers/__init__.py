from fastapi import APIRouter
# from .routers.kiotviet import router as kioviet_router
from .zalo import router as zalo_router

from .kiotviet.router import router as kiotvet_router
from .omicall.router import router as omicall_router
from .demo.main import router as demo

router = APIRouter(prefix="/v1")

router.include_router(zalo_router)
router.include_router(kiotvet_router)
router.include_router(omicall_router)
router.include_router(demo)