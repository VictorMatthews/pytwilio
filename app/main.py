from app.logger import set_uvicorn_loggers
from app.router import router
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup uvicorn loggers before app starts
    set_uvicorn_loggers()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
