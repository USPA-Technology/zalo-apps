from fastapi import APIRouter
from .routers.kiotviet import router as kioviet_router
from .routers.zalo import router as zalo_router
from .routers.omicall import router as omicall


router = APIRouter(prefix="/v1")
router.include_router(zalo_router)
router.include_router(kioviet_router)
router.include_router(omicall)