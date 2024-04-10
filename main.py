import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


DEV_MODE = os.getenv("DEV_MODE") == "true"
HOSTNAME = os.getenv("HOSTNAME")
FOLDER_RESOURCES = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
FOLDER_TEMPLATES = FOLDER_RESOURCES + "templates"

# init FAST API zaloapp
zaloapp = FastAPI(redoc_url= None, docs_url= None)
origins = ["*"]
zaloapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
zaloapp.mount("/resources", StaticFiles(directory=FOLDER_RESOURCES), name="resources")
templates = Jinja2Templates(directory=FOLDER_TEMPLATES)


@zaloapp.get("/", response_class=HTMLResponse)
async def root(request: Request):
    ts = int(time.time())
    data = {"request": request, "HOSTNAME": HOSTNAME, "DEV_MODE": DEV_MODE, 'timestamp': ts}
    return templates.TemplateResponse("index.html", data)

@zaloapp.get("/zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", response_class=HTMLResponse)
async def zalo_verifier(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", data)