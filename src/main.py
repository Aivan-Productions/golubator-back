from loguru import logger
import time
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from db.database import mongodb

from api.routers import all_routers


logger.add("logs/debug.json", format="{time} {level} {message}", level="DEBUG", serialize=True)

app = FastAPI()
add_pagination(app)


for router in all_routers:
    app.include_router(router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} ({process_time:.2f}s)"
    )
    
    return response


@app.on_event("startup")
async def startup_event():
    await mongodb.connect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.on_event("shutdown")
async def shutdown_event():
    await mongodb.close()
