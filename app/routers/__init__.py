from fastapi import APIRouter

from .kiotviet.router import router as kiotvet_router
from .omicall.router import router as omicall_router
from .pancake.router import router as pancake_router
from .zalo.router import router as zalo_router

router = APIRouter(prefix="/v1")

router.include_router(zalo_router)
router.include_router(kiotvet_router)
router.include_router(omicall_router)
router.include_router(pancake_router)
