from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from db.database import mongodb

from api.routers import all_routers


app = FastAPI()
add_pagination(app)


for router in all_routers:
    app.include_router(router)

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
