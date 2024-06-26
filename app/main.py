import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from routers import router
from dependencies import ProcessedItemLogger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# from worker import create_task
from celery.result import AsyncResult

DEV_MODE = os.getenv("DEV_MODE") == "true"
HOSTNAME = os.getenv("HOSTNAME")
FOLDER_RESOURCES = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
FOLDER_TEMPLATES = FOLDER_RESOURCES + "templates"

# init FAST API app
app = FastAPI()
app.include_router(router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/resources", StaticFiles(directory=FOLDER_RESOURCES), name="resources")
templates = Jinja2Templates(directory=FOLDER_TEMPLATES)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    ts = int(time.time())
    data = {"request": request, "HOSTNAME": HOSTNAME, "DEV_MODE": DEV_MODE, 'timestamp': ts}
    return templates.TemplateResponse("index.html", data)

@app.get("/zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", response_class=HTMLResponse)
async def zalo_verifier(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", data)



class ProcessedItemMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: ProcessedItemLogger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response

logger = ProcessedItemLogger()
app.add_middleware(ProcessedItemMiddleware, logger=logger)


