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

from worker import create_task
from celery.result import AsyncResult

DEV_MODE = os.getenv("DEV_MODE") == "true"
HOSTNAME = os.getenv("HOSTNAME")
FOLDER_RESOURCES = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
FOLDER_TEMPLATES = FOLDER_RESOURCES + "templates"

# init FAST API zaloapp
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


# @app.post("/tasks", status_code=201)
# def run_task(payload = Body(...)):
#     task_type = payload["type"]
#     task = create_task.delay(int(task_type))
#     return JSONResponse({"task_id": task.id})

# @app.get("/tasks/{task_id}/")
# def get_status(task_id):
#     task_result = AsyncResult(task_id)
#     result = {
#         "task_id": task_id,
#         "task_status": task_result.status,
#         "task_result": task_result.result
#     }
#     return JSONResponse(result)
